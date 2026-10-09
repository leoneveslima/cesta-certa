// ==========================================
// 1. LÓGICA DA CALCULADORA DE PREÇO POR LITRO
// ==========================================

function setVolumePreset() {
  const preset = document.getElementById('liter-preset').value;
  const customGroup = document.getElementById('custom-volume-group');
  const volumeInput = document.getElementById('liter-volume');

  if (preset === 'custom') {
    customGroup.style.display = 'flex';
  } else {
    customGroup.style.display = 'none';
    volumeInput.value = preset;
  }
  calcularPrecoPorLitro();
}

function calcularPrecoPorLitro() {
  const volume = parseFloat(document.getElementById('liter-volume').value);
  const price = parseFloat(document.getElementById('liter-price').value);
  const resultDiv = document.getElementById('liter-result');

  if (!volume || volume <= 0 || !price || price <= 0) {
    resultDiv.innerHTML = 'Informe o valor unitário para calcular.';
    return;
  }

  // Preço por litro = (Preço Unitário / Volume em ML) * 1000
  const pricePerLiter = (price / volume) * 1000;

  resultDiv.innerHTML = `
    <strong>Preço por Litro:</strong> R$ ${pricePerLiter.toFixed(2).replace('.', ',')}
  `;
}

// ==========================================
// 2. LÓGICA DA RECOMENDAÇÃO DE CHURRASCO
// ==========================================

let churrasItensCalculados = [];

function calcularChurrasco() {
  const pessoas = parseInt(document.getElementById('churras-pessoas').value) || 0;
  const bebedores = parseInt(document.getElementById('churras-bebedores').value) || 0;
  const criancas = parseInt(document.getElementById('churras-criancas').value) || 0;

  // Regras de cálculo (valores aproximados)
  const carneTotalKg = (pessoas * 0.5) + (criancas * 0.25); // 500g adulto, 250g criança
  
  const carneBoivinaKg = carneTotalKg * 0.5; // 50% carne
  const linguiçaKg = carneTotalKg * 0.25;    // 25% linguiça
  const frangoKg = carneTotalKg * 0.25;     // 25% frango

  const paoDeAlho = Math.ceil(pessoas * 2 + criancas * 1); // 2 p/ adulto, 1 p/ criança
  const cervejasLata = bebedores * 8; // 8 latas (350ml) por bebedor
  const refri2L = Math.max(1, Math.ceil((criancas * 0.5 + (pessoas - bebedores) * 0.5) / 2)); // 500ml p/ não-bebedores e crianças

  churrasItensCalculados = [
    { nome: 'Carne Bovina (Picanha/Alcatra/Maminha)', qtd: `${carneBoivinaKg.toFixed(1).replace('.', ',')} kg` },
    { nome: 'Linguiça', qtd: `${linguiçaKg.toFixed(1).replace('.', ',')} kg` },
    { nome: 'Frango (Coxinha/Asa)', qtd: `${frangoKg.toFixed(1).replace('.', ',')} kg` },
    { nome: 'Pão de Alho', qtd: `${paoDeAlho} un` },
    { nome: 'Cerveja (Lata 350ml)', qtd: `${cervejasLata} un` },
    { nome: 'Refrigerante (2 Litros)', qtd: `${refri2L} un` }
  ];

  const container = document.getElementById('churras-results-container');
  container.innerHTML = churrasItensCalculados.map(item => `
    <div class="churras-item">
      <span>${item.nome}</span>
      <strong>${item.qtd}</strong>
    </div>
  `).join('');
}

// Função para integrar com a sua lista de compras existente no localStorage
function adicionarChurrascoALista() {
  if (churrasItensCalculados.length === 0) return;

  // Carrega itens atuais do localStorage (chave mylist_v2)
  let mylistData = JSON.parse(localStorage.getItem('mylist_v2')) || { items: [] };

  churrasItensCalculados.forEach(item => {
    // Adiciona o item à lista se não estiver vazio
    mylistData.items.push({
      id: Date.now() + Math.random(),
      name: `${item.nome} (${item.qtd})`,
      checked: false,
      price: 0,
      quantity: 1
    });
  });

  // Salva de volta no localStorage
  localStorage.setItem('mylist_v2', JSON.stringify(mylistData));

  alert('Itens do churrasco adicionados à sua Lista de Compras!');
  
  // Atualiza a tela/interface da lista se houver uma função de renderização global
  if (typeof renderList === 'function') {
    renderList();
  }
}

// Inicializa os cálculos na abertura
document.addEventListener('DOMContentLoaded', () => {
  calcularChurrasco();
});