// -----------------------------------------------------------------------------
// interacoes.js
// Interações de UI globais do site (sem framework, sem build). Carregado com
// `defer` em templates/base.html, depois do DOM inteiro estar disponível.
// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
// MENU MOBILE
// Alterna a classe .navbar__links--aberto (ver static/css/base.css, seção 10)
// e mantém aria-expanded sincronizado para leitor de tela.
// -----------------------------------------------------------------------------
function inicializarMenuMobile() {
  const botao = document.querySelector(".navbar__alternador");
  const links = document.querySelector(".navbar__links");

  if (!botao || !links) {
    return;
  }

  botao.addEventListener("click", () => {
    const aberto = links.classList.toggle("navbar__links--aberto");
    botao.setAttribute("aria-expanded", String(aberto));
  });
}


// -----------------------------------------------------------------------------
// PONTO DE ENTRADA ÚNICO
// -----------------------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  inicializarMenuMobile();
});
