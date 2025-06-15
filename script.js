//Initialise the list of functions
let functions = [];

// Collect the input
function addFunction() {
    const input = document.getElementById('functionInput');

    // Remove leading/trailing whitespace and check if empty
    const funcStr = input.value.trim();
    if (!funcStr) return;

    //  Add the function input to the list
    // Replace ^ with ** for JS exponentiation
    functions.push(funcStr.replace(/\^/g, '**'));

    //Reset the input
    input.value = '';

    //Render the functions
    renderFunctionList();
    plotFunctions();
}

//Remove a function from the list
function removeFunction(index) {
    // Remove 1 function at the index.
    functions.splice(index, 1);

    // Re-render the function list and plot
    renderFunctionList();
    plotFunctions();
}

//Lists the current functions under the input box
function renderFunctionList() {
    //functionList is a div element in the HTML
    const list = document.getElementById('functionList');
    //Clear the current list
    list.innerHTML = '';
    //Go through the function list and create a div for each function
    functions.forEach((f, i) => {
        //Creates a new div element
        const div = document.createElement('div');
        //Styles the new div
        div.style.display = 'flex';
        div.style.alignItems = 'center';
        div.style.gap = '8px';
        div.innerHTML = `<span style="flex:1;"> ${f.replace(/\*\*/g, '^')} </span><button style="background:#393e46;" onclick="removeFunction(${i})">✕</button>`;
        //Add the new div to the functionList div.
        list.appendChild(div);
    });
}

function plotFunctions() {
    // Get the group order
    const groupOrder = parseInt(document.getElementById('groupOrder').value);

    //Plot
    //Initialise the x values. Use the values from -groupOrder to groupOrder
    //Use the toggles to determine what is DISPLAYED. Always compute all. Simplifies the logic.
    const x = [];
    for (let i = -groupOrder; i <= groupOrder; i += 1) x.push(i);

    // Create a new list called traces and add the functions into it after modification
    const traces = functions.map(fstr => {
        let y = [];
        //Iterate through the x values and calculate the y values
        // Use a try-catch to handle any errors in the function evaluation
        for (let i = 0; i < x.length; i++) {
            try {
                //Function creates a javascript function from the string
                //Then we pass it x[i], reduce it mod the group order and add that to the y array
                y.push(Function('x', `return ${fstr}`)(x[i])%groupOrder);
            } catch {
                y.push(NaN);
            }
        }
        //Added to the traces array
        const connect = document.getElementById('toggleConnecting').checked;
        if (connect){
            //If connect lines is checked, return a line trace
            return { x, y, mode: 'lines', name: fstr };
        }else {
            //If connect lines is not checked, return a marker trace
            return { x, y, mode: 'markers', name: fstr };
        }
    });

    //Plot
    Plotly.newPlot('plot', traces, {
        margin: { t: 30 },
        xaxis: { title: 'x', zeroline: true, showgrid: true },
        yaxis: { title: 'y', zeroline: true, showgrid: true },

        //Puts the legend at the top left
        legend: { x: 0, y: 1 },
        plot_bgcolor: '#fff',
        paper_bgcolor: '#fff',
    });
}

// Initial render
renderFunctionList();
plotFunctions();