import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, random_split
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 📂 Configurações do projeto
data_dir = r'C:\Users\usuario\Desktop\projetos\Oikos\dataset\dataset-resized\dataset-resized'
model_path = "modelo_oikos.pt"
batch_size = 16
learning_rate = 0.001
num_epochs = 10

# 🧹 Transformações para treino (com data augmentation)
train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(p=0.5),  # Augmentation
    transforms.RandomRotation(10),            # Augmentation
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225])
])

# 🧹 Transformações para teste (sem augmentation)
test_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225])
])

def prepare_data():
    """
    Prepara e divide os dados em treino e teste (80/20)
    """
    print("📥 Carregando dataset...")
    
    # Carregar dataset completo
    full_dataset = datasets.ImageFolder(root=data_dir, transform=train_transform)
    
    # Calcular tamanhos para split 80/20
    total_size = len(full_dataset)
    train_size = int(0.8 * total_size)
    test_size = total_size - train_size
    
    # Dividir dataset
    train_dataset, test_dataset = random_split(full_dataset, [train_size, test_size])
    
    # Aplicar transformações específicas para teste
    test_dataset.dataset = datasets.ImageFolder(root=data_dir, transform=test_transform)
    
    # Criar DataLoaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    
    print(f"✅ Dataset carregado:")
    print(f"   - Total de amostras: {total_size}")
    print(f"   - Treino: {train_size} amostras")
    print(f"   - Teste: {test_size} amostras")
    print(f"   - Classes: {full_dataset.classes}")
    
    return train_loader, test_loader, full_dataset.classes

def create_model(num_classes):
    """
    Cria o modelo EfficientNetB0 com transfer learning
    """
    print("🧠 Configurando modelo EfficientNetB0...")
    
    # Carregar modelo pré-treinado
    model = models.efficientnet_b0(pretrained=True)
    
    # Congelar layers iniciais para transfer learning
    for param in model.features.parameters():
        param.requires_grad = False
    
    # Substituir classificador final
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)
    
    print(f"✅ Modelo configurado para {num_classes} classes")
    return model

def train_model(model, train_loader, criterion, optimizer, device):
    """
    Treina o modelo e retorna histórico de loss
    """
    model.train()
    train_losses = []
    
    print("🚀 Iniciando treinamento...")
    
    for epoch in range(num_epochs):
        running_loss = 0.0
        correct_predictions = 0
        total_samples = 0
        
        for batch_idx, (inputs, labels) in enumerate(train_loader):
            inputs, labels = inputs.to(device), labels.to(device)
            
            # Forward pass
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            
            # Backward pass
            loss.backward()
            optimizer.step()
            
            # Estatísticas
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total_samples += labels.size(0)
            correct_predictions += (predicted == labels).sum().item()
            
            # Log a cada 10 batches
            if batch_idx % 10 == 0:
                print(f"   Batch [{batch_idx}/{len(train_loader)}] - Loss: {loss.item():.4f}")
        
        # Métricas da época
        epoch_loss = running_loss / len(train_loader)
        epoch_acc = 100 * correct_predictions / total_samples
        train_losses.append(epoch_loss)
        
        print(f"Época [{epoch+1}/{num_epochs}]:")
        print(f"   - Loss: {epoch_loss:.4f}")
        print(f"   - Acurácia Treino: {epoch_acc:.2f}%\n")
    
    return train_losses

def evaluate_model(model, test_loader, classes, device):
    """
    Avalia o modelo no conjunto de teste e calcula métricas
    """
    model.eval()
    all_predictions = []
    all_labels = []
    
    print("🔍 Avaliando modelo no conjunto de teste...")
    
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            
            all_predictions.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    # Calcular métricas
    accuracy = accuracy_score(all_labels, all_predictions)
    f1 = f1_score(all_labels, all_predictions, average='weighted')
    
    print("📊 Resultados da Avaliação:")
    print(f"   - Acurácia: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"   - F1-Score: {f1:.4f}")
    
    # Relatório detalhado
    print("\n📋 Relatório de Classificação:")
    print(classification_report(all_labels, all_predictions, target_names=classes))
    
    # Matriz de confusão
    cm = confusion_matrix(all_labels, all_predictions)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=classes, yticklabels=classes)
    plt.title('Matriz de Confusão')
    plt.xlabel('Predição')
    plt.ylabel('Real')
    plt.tight_layout()
    plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return accuracy, f1, all_predictions, all_labels

def fine_tune_model(model, train_loader, test_loader, classes, device):
    """
    Fine-tuning: descongelar algumas camadas e treinar com learning rate menor
    """
    print("🔧 Iniciando fine-tuning...")
    
    # Descongelar últimas camadas do backbone
    for param in model.features[-3:].parameters():
        param.requires_grad = True
    
    # Novo otimizador com learning rate menor
    optimizer_ft = optim.Adam(model.parameters(), lr=0.0001)
    criterion = nn.CrossEntropyLoss()
    
    # Treinar por mais algumas épocas
    for epoch in range(3):
        model.train()
        running_loss = 0.0
        
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer_ft.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer_ft.step()
            
            running_loss += loss.item()
        
        print(f"Fine-tuning Época [{epoch+1}/3] - Loss: {running_loss/len(train_loader):.4f}")
    
    # Avaliar após fine-tuning
    print("\n🎯 Avaliação após fine-tuning:")
    accuracy_ft, f1_ft, _, _ = evaluate_model(model, test_loader, classes, device)
    
    return accuracy_ft, f1_ft

def main():
    """
    Função principal que executa todo o pipeline
    """
    print("🚀 Iniciando projeto de classificação de imagens")
    print("=" * 50)
    
    # Configurar device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"💻 Usando device: {device}")
    
    # Preparar dados
    train_loader, test_loader, classes = prepare_data()
    num_classes = len(classes)
    
    # Criar modelo
    model = create_model(num_classes)
    model = model.to(device)
    
    # Configurar treinamento
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # Treinamento inicial
    train_losses = train_model(model, train_loader, criterion, optimizer, device)
    
    # Avaliação inicial
    print("\n" + "="*50)
    accuracy_initial, f1_initial, _, _ = evaluate_model(model, test_loader, classes, device)
    
    # Fine-tuning
    print("\n" + "="*50)
    accuracy_final, f1_final = fine_tune_model(model, train_loader, test_loader, classes, device)
    
    # Comparação de resultados
    print("\n" + "="*50)
    print("📈 COMPARAÇÃO DE RESULTADOS:")
    print(f"   Antes do fine-tuning:")
    print(f"     - Acurácia: {accuracy_initial:.4f}")
    print(f"     - F1-Score: {f1_initial:.4f}")
    print(f"   Após fine-tuning:")
    print(f"     - Acurácia: {accuracy_final:.4f}")
    print(f"     - F1-Score: {f1_final:.4f}")
    print(f"   Melhoria:")
    print(f"     - Acurácia: {accuracy_final - accuracy_initial:+.4f}")
    print(f"     - F1-Score: {f1_final - f1_initial:+.4f}")
    
    # Salvar modelo
    torch.save(model.state_dict(), model_path)
    print(f"\n✅ Modelo salvo como '{model_path}'")
    
    # Plotar curva de treinamento
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(train_losses) + 1), train_losses, 'b-', label='Loss de Treinamento')
    plt.xlabel('Época')
    plt.ylabel('Loss')
    plt.title('Curva de Treinamento')
    plt.legend()
    plt.grid(True)
    plt.savefig('training_curve.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\n🎉 Modelo finalizado com sucesso!")

if __name__ == "__main__":
    main()
