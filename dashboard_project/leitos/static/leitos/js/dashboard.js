// Funções utilitárias
async function fetchJSON(path) {
  const resp = await fetch(path);
  if (!resp.ok) throw new Error("Erro na API: " + resp.status);
  return resp.json();
}

async function safeFetch(path) {
  try {
    return await fetchJSON(path);
  } catch (e) {
    return await fetchJSON("/dashboard" + path);
  }
}

// Gráficos
async function drawZonaLeitos(cep = "", zona = "") {
  let url = '/api/zona_leitos/';
  const params = new URLSearchParams();
  if (cep) params.append('cep', cep);
  if (zona) params.append('zone', zona);
  if ([...params].length) url += '?' + params.toString();

  try {
    const data = await safeFetch(url);
    if (!Array.isArray(data)) return console.error("Formato inesperado:", data);
    const zonas = data.map(item => item.zone);
    const leitosExist = data.map(item => item.leitos_exist);
    const leitosSus = data.map(item => item.leitos_sus);

    const trace1 = { x: zonas, y: leitosExist, name: "Leitos Totais", type: "bar", marker: { color: "#1F77B4" } };
    const trace2 = { x: zonas, y: leitosSus, name: "Leitos SUS", type: "bar", marker: { color: "#ff7f0e" } };
    const layout = { barmode: "group", title: "Leitos Totais x Leitos SUS", height: 360, margin: { t:50,r:20,l:50,b:50 }, xaxis:{title:"Região"}, yaxis:{title:"Quantidade de Leitos"} };
    Plotly.newPlot("chart-zona-leitos", [trace1, trace2], layout, { responsive: true });
  } catch(e) { console.error("Erro ao carregar gráfico de leitos existentes x leitos SUS:", e); }
}

async function drawZonaEspecialidades(cep = "", zona = "") {
  let url = '/api/zona_especialidades/';
  const params = new URLSearchParams();
  if (cep) params.append('cep', cep);
  if (zona) params.append('zone', zona);
  if ([...params].length) url += '?' + params.toString();

  try {
    const data = await safeFetch(url);
    if (!Array.isArray(data)) return console.error("Formato inesperado:", data);

    const zonas = data.map(item => item.zone);
    const leitosUtiAdulSus = data.map(item => item.leitos_uti_adulto_sus);
    const leitosUtiCoroSus = data.map(item => item.leitos_uti_coronariana_sus);
    const leitosUtiNeonSus = data.map(item => item.leitos_uti_neonatal_sus);
    const leitosUtiPediSus = data.map(item => item.leitos_uti_pediatrico_sus);
    const leitosUtiQueiSus = data.map(item => item.leitos_uti_queimado_sus);

    const traces = [
      {x: zonas,y: leitosUtiAdulSus,name:"UTI Adulto SUS",type:"bar",marker:{color:"#1f77b4"}},
      {x: zonas,y: leitosUtiCoroSus,name:"UTI Coronariana SUS",type:"bar",marker:{color:"#d62728"}},
      {x: zonas,y: leitosUtiNeonSus,name:"UTI Neonatal SUS",type:"bar",marker:{color:"#9467bd"}},
      {x: zonas,y: leitosUtiPediSus,name:"UTI Pediátrico SUS",type:"bar",marker:{color:"#ff7f0e"}},
      {x: zonas,y: leitosUtiQueiSus,name:"UTI Queimados SUS",type:"bar",marker:{color:"#2ca02c"}}
    ];

    const layout = { barmode:"group", title:"Especialidades por Região", height:360, margin:{t:50,r:20,l:50,b:50}, xaxis:{title:"Região"}, yaxis:{title:"Quantidade de UTIs SUS"} };
    Plotly.newPlot("chart-zona-especialidades", traces, layout, { responsive:true });
  } catch(e) { console.error("Erro ao carregar dados de especialidades UTIs:", e); }
}

async function drawGraficoEvolucaoLeitos(cep = "", zona = "") {
  let url = '/api/evolucao_leitos/';
  const params = new URLSearchParams();
  if (cep) params.append('cep', cep);
  if (zona) params.append('zone', zona);
  if ([...params].length) url += '?' + params.toString();

  try {
    const data = await safeFetch(url);
    const registros = Array.isArray(data)? data: data.results || [];
    if (!registros.length) { document.getElementById('chart-evolucao-leitos').innerHTML="Nenhum dado encontrado"; return; }

    // Função para traduzir mês/ano para pt-BR
            function formatMonthPtBr(yyyy_mm) {
                const meses = [
                    "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
                    "Jul", "Ago", "Set", "Out", "Nov", "Dez"
                ];
                if (!yyyy_mm) return "";
                const [year, month] = yyyy_mm.split(" ");
                const mIndex = parseInt(month, 10) - 1;
                if (isNaN(mIndex) || mIndex < 0 || mIndex > 11) return yyyy_mm;
                return `${meses[mIndex]}/${year}`;
            }

    const zonasSet=[...new Set(registros.map(d=>d.zone))];
    const mesesOriginais=[...new Set(registros.map(d=>d.comp))].sort();
    const meses=mesesOriginais.map(m=>formatMonthPtBr(m));

    const cores=['#1f77b4','#d62728','#9467bd','#ff7f0e','#2ca02c'];
    const traces=[];
    zonasSet.forEach((z,idx)=>{
      const dadosZona=registros.filter(d=>d.zone===z);
      const y_exist=mesesOriginais.map(m=>{const i=dadosZona.find(d=>d.comp===m);return i?i.leitos_exist:0;});
      const y_sus=mesesOriginais.map(m=>{const i=dadosZona.find(d=>d.comp===m);return i?i.leitos_sus:0;});
      traces.push({x:meses,y:y_exist,mode:'lines+markers',name:`Leitos Totais - ${z}`,line:{shape:'spline',width:2.5,color:cores[idx%cores.length]},marker:{size:5}});
      traces.push({x:meses,y:y_sus,mode:'lines+markers',name:`Leitos SUS - ${z}`,line:{shape:'spline',dash:'dash',width:2.5,color:cores[idx%cores.length]},marker:{size:5}});
    });

    const layout={title:'Evolução Mensal de Leitos Totais x Leitos SUS por Região',xaxis:{title:'Mês / Ano',tickangle:-30},yaxis:{title:'Quantidade de Leitos'},height:430,hovermode:'x unified',legend:{orientation:"h",y:-0.25},margin:{t:60,b:80}};
    Plotly.newPlot('chart-evolucao-leitos',traces,layout,{responsive:true});
  } catch(e){console.error("Erro ao carregar gráfico de evolução:", e); document.getElementById('chart-evolucao-leitos').innerHTML="Erro ao carregar gráfico de evolução";}
}

// Inicialização
function inicializarGraficos(cep="", zona="") {
  drawZonaLeitos(cep,zona);
  drawZonaEspecialidades(cep,zona);
  drawGraficoEvolucaoLeitos(cep,zona);
}

// Tabela
function buildTable(rows) {
  const container = document.getElementById("table-estabs");
  if (!rows || rows.length === 0) {
    container.innerHTML = "<div class='alert alert-warning text-center m-2'>Nenhum hospital encontrado.</div>";
    return;
  }
  const table = document.createElement("table");
  table.className = "table table-striped table-sm";
  const headers = ["Município", "Zona", "CEP", "Hospital", "Leitos Existentes", "Leitos SUS"];
  const displayNames = ["Município", "Região", "CEP", "Hospital", "Leitos Totais", "Leitos SUS"];
  const thead = document.createElement("thead");
  thead.innerHTML = "<tr>" + displayNames.map(h => `<th>${h}</th>`).join("") + "</tr>";
  table.appendChild(thead);
  const tbody = document.createElement("tbody");
  rows.forEach(r => {
    const tr = document.createElement("tr");
    headers.forEach(h => {
      const td = document.createElement("td");
      td.textContent = r[h] !== undefined ? r[h] : "";
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);
  container.innerHTML = "";
  container.appendChild(table);
}

let currentPage = 1;
let currentPageSize = 25;
let currentTotalPages = 1;

async function loadTable(cep = "", zona = "", page = 1, page_size = 25){
  let url = `/api/estabelecimentos/?page=${page}&page_size=${page_size}`;
  const params = new URLSearchParams();
  if (cep) params.append('cep', cep);
  if (zona) params.append('zone', zona);
  if ([...params].length) url += '&' + params.toString();

  const data = await safeFetch(url);
  if(!data){document.getElementById("table-estabs").innerHTML="<p>Erro ao carregar tabela.</p>"; return;}

  buildTable(data.results);
  currentPage = data.page;
  currentPageSize = data.page_size;
  currentTotalPages = data.total_pages;
  document.getElementById("table-info").textContent = `Página ${currentPage} de ${currentTotalPages} — ${data.total} registros`;
  document.getElementById("prev-page").disabled = (currentPage <= 1);
  document.getElementById("next-page").disabled = (currentPage >= currentTotalPages);
}

// Event listeners
document.getElementById("btn-apply").addEventListener("click", async () => {
  const cep = document.getElementById("filter-cep").value.trim();
  const zona = document.getElementById("filter-zone").value.trim();
  currentPage = 1;
  await inicializarGraficos(cep,zona);
  await loadTable(cep,zona,currentPage,currentPageSize);
});

document.getElementById("btn-clear").addEventListener("click", async () => {
  document.getElementById("filter-cep").value = "";
  document.getElementById("filter-zone").value = "";
  currentPage = 1;
  await inicializarGraficos();
  await loadTable("", "", currentPage, currentPageSize);
});

document.getElementById("prev-page").addEventListener("click", async () => {
  if(currentPage > 1){
    currentPage -= 1;
    const cep = document.getElementById("filter-cep").value.trim();
    const zona = document.getElementById("filter-zone").value.trim();
    await loadTable(cep,zona,currentPage,currentPageSize);
  }
});

document.getElementById("next-page").addEventListener("click", async () => {
  if(currentPage < currentTotalPages){
    currentPage += 1;
    const cep = document.getElementById("filter-cep").value.trim();
    const zona = document.getElementById("filter-zone").value.trim();
    await loadTable(cep,zona,currentPage,currentPageSize);
  }
});

document.getElementById("select-page-size").addEventListener("change", async (e) => {
  currentPageSize = Number(e.target.value);
  currentPage = 1;
  const cep = document.getElementById("filter-cep").value.trim();
  const zona = document.getElementById("filter-zone").value.trim();
  await loadTable(cep,zona,currentPage,currentPageSize);
});

document.getElementById("btn-export").addEventListener("click", async () => {
  const cep = document.getElementById("filter-cep").value.trim();
  const zona = document.getElementById("filter-zone").value.trim();
  let url = "/api/estabelecimentos/export/";
  const params = new URLSearchParams();
  if (cep) params.append('cep', cep);
  if (zona) params.append('zone', zona);
  if ([...params].length) url += '?' + params.toString();
  window.location = url;
});

// Filtros e inicialização
document.addEventListener("DOMContentLoaded", async function () {
  const filterZona = document.getElementById("filter-zone");
  const filterCep = document.getElementById("filter-cep");

  // Preenche as opções de Regiões
  try {
    const data = await safeFetch("/api/filters/");
    const zones = data.zones || [];
    filterZona.innerHTML = `<option value="">Todas as Regiões</option>`;
    zones.forEach((z) => {
      const opt = document.createElement("option");
      opt.value = z;
      opt.textContent = z;
      filterZona.appendChild(opt);
    });
  } catch (err) {
    console.error("Erro ao carregar regiões:", err);
  }

  inicializarGraficos();
  loadTable("", "", currentPage, currentPageSize);
});
