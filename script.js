function plotFunction() {
            const funcStr = document.getElementById('functionInput').value;
            const x = [];
            const y = [];
            for (let i = -10; i <= 10; i += 0.1) {
                x.push(i);
                try {
                    y.push(eval(funcStr.replace(/x/g, `(${i})`)));
                } catch {
                    y.push(NaN);
                }
            }
            Plotly.newPlot('plot', [{ x, y, mode: 'lines', name: funcStr }], { margin: { t: 30 }, xaxis: { title: 'x' }, yaxis: { title: 'y' } });
        }