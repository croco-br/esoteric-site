// Rodadas do oráculo — planetas, signos e números, cada um com sua sentença.
const planets = [
    { symbol: '☉', name: 'Sol', desc: 'Vitalidade e aquilo que ilumina a questão.' },
    { symbol: '☽', name: 'Lua', desc: 'Intuição, memória e o que ainda não foi dito.' },
    { symbol: '☿', name: 'Mercúrio', desc: 'Palavras, contratos, viagens e recados.' },
    { symbol: '♀', name: 'Vênus', desc: 'Afeição, acordos, prazer e o que se atrai.' },
    { symbol: '♂', name: 'Marte', desc: 'Coragem, disputa e o impulso de agir.' },
    { symbol: '♃', name: 'Júpiter', desc: 'Expansão, sorte generosa e conselhos de quem sabe mais.' },
    { symbol: '♄', name: 'Saturno', desc: 'Tempo, limite, paciência e dívidas que vencem.' },
    { symbol: '♅', name: 'Urano', desc: 'Ruptura, novidade e o imprevisto que reorganiza tudo.' },
    { symbol: '♆', name: 'Netuno', desc: 'Sonho, fé e a névoa que embaralha os fatos.' },
    { symbol: '♇', name: 'Plutão', desc: 'Fim de ciclo, poder e a verdade debaixo do tapete.' },
    { symbol: '☊', name: 'Nodo Norte', desc: 'O caminho que cresce quando você o segue.' },
    { symbol: '☋', name: 'Nodo Sul', desc: 'Hábitos antigos e o que se repete sem perceber.' }
];

const zodiac = [
    { symbol: '♈', name: 'Áries', desc: 'Começo impetuoso; melhor não esperar.' },
    { symbol: '♉', name: 'Touro', desc: 'Passo firme; o valor está no que dura.' },
    { symbol: '♊', name: 'Gêmeos', desc: 'Duas versões do mesmo caso; ouça as duas.' },
    { symbol: '♋', name: 'Câncer', desc: 'Casa, família e o cuidado que sustenta.' },
    { symbol: '♌', name: 'Leão', desc: 'Vista a coroa; a cena pede presença.' },
    { symbol: '♍', name: 'Virgem', desc: 'O detalhe pequeno decide o todo.' },
    { symbol: '♎', name: 'Libra', desc: 'Pesa os dois pratos antes de fechar.' },
    { symbol: '♏', name: 'Escorpião', desc: 'Fundo do poço e a força de sair dele.' },
    { symbol: '♐', name: 'Sagitário', desc: 'Horizonte largo; vale apostar longe.' },
    { symbol: '♑', name: 'Capricórnio', desc: 'Escada degrau por degrau, sem pressa.' },
    { symbol: '♒', name: 'Aquário', desc: 'O inesperado chega por pessoas diferentes.' },
    { symbol: '♓', name: 'Peixes', desc: 'Corrente subterrânea; confie no que se sente.' }
];

const numbers = [
    { symbol: '1', name: 'Um', desc: 'Tudo começa por uma decisão sua.' },
    { symbol: '2', name: 'Dois', desc: 'Ninguém atravessa isso sozinho.' },
    { symbol: '3', name: 'Três', desc: 'Uma terceira via que ainda não apareceu.' },
    { symbol: '4', name: 'Quatro', desc: 'Fundamento, quatro paredes, trabalho lento.' },
    { symbol: '5', name: 'Cinco', desc: 'Mudança no meio do caminho; adapte-se.' },
    { symbol: '6', name: 'Seis', desc: 'Harmonia devolvida depois do atrito.' },
    { symbol: '7', name: 'Sete', desc: 'Recolhimento e estudo antes da resposta.' },
    { symbol: '8', name: 'Oito', desc: 'Colheita do que foi semeado — bom ou ruim.' },
    { symbol: '9', name: 'Nove', desc: 'Fim de capítulo; deixe o que cumpriu seu papel.' },
    { symbol: '10', name: 'Dez', desc: 'Ciclo completo; o próximo já se anuncia.' },
    { symbol: '11', name: 'Onze', desc: 'Aviso e segunda chance na mesma mensagem.' },
    { symbol: '12', name: 'Doze', desc: 'As doze casas: a roda inteira gira com você.' }
];

const WHEELS = [planets, zodiac, numbers];
const GLYPH_IDS = ['dado1-glyph', 'dado2-glyph', 'dado3-glyph'];
const NAME_IDS = ['dado1-nome', 'dado2-nome', 'dado3-nome'];
const DESC_IDS = ['dado1-desc', 'dado2-desc', 'dado3-desc'];
const SHUFFLE_MS = 700;
const SHUFFLE_TICK_MS = 80;

function pick(wheel) {
    return wheel[Math.floor(Math.random() * wheel.length)];
}

function shuffleGlyphs() {
    GLYPH_IDS.forEach((id) => {
        const el = document.getElementById(id);
        el.classList.add('is-shuffling');
        el.classList.remove('is-settled');
        el.textContent = '?';
    });
}

function drawPair(wheel, glyphsEl) {
    const a = pick(wheel);
    glyphsEl.textContent = a.symbol;
    glyphsEl.classList.remove('is-shuffling');
    glyphsEl.classList.add('is-settled');
    return a;
}

function rollDice() {
    const question = document.getElementById('situacao');
    const helper = document.getElementById('consulta-ajuda');
    const button = document.getElementById('consultar');
    const reading = document.getElementById('leitura');
    const readingText = document.getElementById('leitura-texto');

    const situacao = question.value.trim();
    if (!situacao) {
        helper.dataset.role = 'error';
        helper.textContent = 'Escreva a situação antes de consultar os oráculos.';
        question.setAttribute('aria-invalid', 'true');
        question.focus();
        return;
    }
    question.removeAttribute('aria-invalid');
    helper.dataset.role = 'hint';
    helper.textContent = 'Os oráculos giram…';

    button.setAttribute('data-state', 'loading');
    button.setAttribute('aria-disabled', 'true');
    button.disabled = true;
    reading.hidden = true;
    shuffleGlyphs();

    const timers = [];
    timers.push(setInterval(() => {
        GLYPH_IDS.forEach((id, i) => {
            document.getElementById(id).textContent = pick(WHEELS[i]).symbol;
        });
    }, SHUFFLE_TICK_MS));

    setTimeout(() => {
        timers.forEach(clearInterval);
        const drawn = WHEELS.map((wheel, i) => drawPair(wheel, document.getElementById(GLYPH_IDS[i])));
        drawn.forEach((item, i) => {
            document.getElementById(NAME_IDS[i]).textContent = item.name;
            document.getElementById(DESC_IDS[i]).textContent = item.desc;
        });
        readingText.textContent = buildReading(drawn);
        reading.hidden = false;
        button.disabled = false;
        button.removeAttribute('aria-disabled');
        button.removeAttribute('data-state');
        helper.textContent = 'Consulte de novo quantas vezes quiser.';
    }, SHUFFLE_MS);
}

function buildReading([planet, sign, number]) {
    return (
        'Com a situação “' + questionText() + '”, ' +
        planet.name + ' fala ' + sign.name + ' — ' + planet.desc.toLowerCase().replace(/\.$/, '') +
        ', e o modo de ' + sign.name + ' é ' + sign.desc.toLowerCase() +
        ' O número ' + number.name.toLowerCase() + ' fecha a tiragem: ' + number.desc
    );
}

function questionText() {
    return document.getElementById('situacao').value.trim().replace(/["“”]/g, '');
}
