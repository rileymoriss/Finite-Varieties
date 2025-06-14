let functions = [];

function addFunction() {
    const input = document.getElementById('functionInput');
    const funcStr = input.value.trim();
    if (!funcStr) return;
    functions.push(funcStr);
    input.value = '';
    renderFunctionList();
    plotFunctions();
}

function removeFunction(index) {
    functions.splice(index, 1);
    renderFunctionList();
    plotFunctions();
}

function renderFunctionList() {
    const list = document.getElementById('functionList');
    list.innerHTML = `<div class="function-input">
        <input type="text" id="functionInput" placeholder="e.g. sin(x)" />
        <button onclick="addFunction()">Add</button>
    </div>`;
    functions.forEach((f, i) => {
        const div = document.createElement('div');
        div.style.display = 'flex';
        div.style.alignItems = 'center';
        div.style.gap = '8px';
        div.innerHTML = `<span style="flex:1;">${f}</span><button style="background:#393e46;" onclick="removeFunction(${i})">✕</button>`;
        list.appendChild(div);
    });
}

function plotFunctions() {
    const x = [];
    for (let i = -10; i <= 10; i += 0.05) x.push(i);
    const traces = functions.map(fstr => {
        let y = [];
        for (let i = 0; i < x.length; i++) {
            try {
                // Replace ^ with ** for JS exponentiation, and allow common math functions
                let expr = fstr.replace(/\^/g, '**')
                    .replace(/sin/g, 'Math.sin')
                    .replace(/cos/g, 'Math.cos')
                    .replace(/tan/g, 'Math.tan')
                    .replace(/exp/g, 'Math.exp')
                    .replace(/log/g, 'Math.log')
                    .replace(/abs/g, 'Math.abs');
                y.push(Function('x', `return ${expr}`)(x[i]));
            } catch {
                y.push(NaN);
            }
        }
        return { x, y, mode: 'lines', name: fstr };
    });
    Plotly.newPlot('plot', traces, {
        margin: { t: 30 },
        xaxis: { title: 'x', zeroline: true, showgrid: true },
        yaxis: { title: 'y', zeroline: true, showgrid: true },
        legend: { x: 0, y: 1 },
        plot_bgcolor: '#fff',
        paper_bgcolor: '#fff',
    });
}

// Initial render
renderFunctionList();
plotFunctions();