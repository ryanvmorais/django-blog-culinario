// -----------------------------------------------------------------------------
// interacoes.js
// Interações de UI globais do site (sem framework, sem build). Carregado com
// `defer` em templates/base.html, depois do DOM inteiro estar disponível.
// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
// MENU MOBILE
// Alterna a classe .navbar__links--aberto (ver static/css/base.css, seção 10)
// e mantém aria-expanded e aria-label sincronizados para leitor de tela.
// Teclado (spec 008, RF-06): abrir leva o foco ao primeiro link, Esc fecha e
// devolve o foco ao botão, e clicar fora da barra fecha sem mexer no foco.
// -----------------------------------------------------------------------------
function inicializarMenuMobile() {
  const botao = document.querySelector(".navbar__alternador");
  const links = document.querySelector(".navbar__links");
  const barra = document.querySelector(".navbar");

  if (!botao || !links || !barra) {
    return;
  }

  const estaAberto = () => links.classList.contains("navbar__links--aberto");

  const abrirMenu = () => {
    links.classList.add("navbar__links--aberto");
    botao.setAttribute("aria-expanded", "true");
    botao.setAttribute("aria-label", "Fechar menu de navegação");
    const primeiroLink = links.querySelector("a");
    if (primeiroLink) {
      primeiroLink.focus();
    }
  };

  // devolverFoco: com Esc o foco volta ao botão; com clique fora, o visitante
  // já escolheu outro lugar e o foco fica onde ele clicou.
  const fecharMenu = ({ devolverFoco }) => {
    links.classList.remove("navbar__links--aberto");
    botao.setAttribute("aria-expanded", "false");
    botao.setAttribute("aria-label", "Abrir menu de navegação");
    if (devolverFoco) {
      botao.focus();
    }
  };

  botao.addEventListener("click", () => {
    if (estaAberto()) {
      fecharMenu({ devolverFoco: true });
    } else {
      abrirMenu();
    }
  });

  document.addEventListener("keydown", (evento) => {
    if (evento.key === "Escape" && estaAberto()) {
      fecharMenu({ devolverFoco: true });
    }
  });

  document.addEventListener("click", (evento) => {
    if (estaAberto() && !barra.contains(evento.target)) {
      fecharMenu({ devolverFoco: false });
    }
  });
}


// -----------------------------------------------------------------------------
// PONTO DE ENTRADA ÚNICO
// -----------------------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  inicializarMenuMobile();
});
