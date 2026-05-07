function addCustomFunction() {

    let terms = [];

    // Read operators
    let op1 = document.getElementById("operator1").value;
    let op2 = document.getElementById("operator2").value;

    // Read terms
    let f1 = document.getElementById("cfunc1").value;
    let d1 = document.getElementById("cfunc2").value;

    let f2 = document.getElementById("cfunc3").value;
    let d2 = document.getElementById("cfunc4").value;

    let f3 = document.getElementById("cfunc5").value;
    let d3 = document.getElementById("cfunc6").value;

    // Build equation dynamically
    let funcStr = "";

    // TERM 1
    if (f1 && d1) {
        funcStr += `${f1}/${d1}`;
    }

    // TERM 2
    if (f2 && d2) {

        if (funcStr !== "") {
            funcStr += ` ${op1} `;
        }

        funcStr += `${f2}/${d2}`;
    }

    // TERM 3
    if (f3 && d3) {

        if (funcStr !== "") {
            funcStr += ` ${op2} `;
        }

        funcStr += `${f3}/${d3}`;
    }

    // Validation
    if (funcStr.trim() === "") {
        alert("Please select at least one valid term");
        return;
    }

    // LocalStorage
    let saved = JSON.parse(localStorage.getItem("customFunctions")) || [];

    // Prevent duplicate
    if (saved.includes(funcStr)) {
        alert("Function already exists!");
        return;
    }

    // Save
    saved.push(funcStr);

    localStorage.setItem(
        "customFunctions",
        JSON.stringify(saved)
    );

    // Update dropdown + table
    addFunctionToDropdown(funcStr);

    renderFunctionTable();

    // Optional close popup
    // document.getElementById("myModalFun").style.display = "none";
}
function addCustomFunction333() {

    let terms = [];

    function addTerm(f, d) {
        if (f && d) {
            terms.push(`${f}/${d}`);
        }
    }

    // Read values
    addTerm(cfunc1.value, cfunc2.value);
    addTerm(cfunc3.value, cfunc4.value);
    addTerm(cfunc5.value, cfunc6.value);

    // ❌ If nothing selected
    if (terms.length === 0) {
        alert("Please select at least one valid term");
        return;
    }

    // Build final function
    let funcStr = terms.join(" + ");

    // Get existing
    let saved = JSON.parse(localStorage.getItem("customFunctions")) || [];

    // ✅ Prevent duplicate
    if (saved.includes(funcStr)) {
        alert("Function already exists!");
        return;
    }

    // Save
    saved.push(funcStr);
    localStorage.setItem("customFunctions", JSON.stringify(saved));

    // Update UI
    addFunctionToDropdown(funcStr);
    renderFunctionTable();

    // Close popup
    // document.getElementById("myModalFun").style.display = "none";
}
function addCustomFunction22() {

    // Get values
    let f1 = document.getElementById("cfunc1").value;
    let d1 = document.getElementById("cfunc2").value;

    let f2 = document.getElementById("cfunc3").value;
    let d2 = document.getElementById("cfunc4").value;

    let f3 = document.getElementById("cfunc5").value;
    let d3 = document.getElementById("cfunc6").value;

    // Build function string
    let funcStr = `${f1}/${d1} + ${f2}/${d2} + ${f3}/${d3}`;

    // Get existing list from localStorage
    let saved = JSON.parse(localStorage.getItem("customFunctions")) || [];

    // Add new function
    saved.push(funcStr);

    // Save back
    localStorage.setItem("customFunctions", JSON.stringify(saved));

    // Add to dropdown UI
    addFunctionToDropdown(funcStr);
    renderFunctionTable();   // 👈 update table

    // Close modal
    // document.getElementById("myModalFun").style.display = "none";
}
function addFunctionToDropdown(funcStr) {
    let dropdown = document.getElementById("func");

    let option = document.createElement("option");
    option.text = funcStr;
    // option.value = funcStr;   // store full string
    option.value = funcStr.replaceAll("²", "^2").replaceAll("³", "^3");

    dropdown.appendChild(option);

    // dropdown.value = funcStr; // select newly added
    dropdown.value = option.value;
}
window.addEventListener("load", function () {
    let saved = JSON.parse(localStorage.getItem("customFunctions")) || [];

    saved.forEach(func => {
        // addFunctionToDropdown(func);
        reloadDropdown();
        renderFunctionTable();
    });
});
function renderFunctionTable() {
    let table = document.getElementById("functionTableBody");
    table.innerHTML = "";

    let saved = JSON.parse(localStorage.getItem("customFunctions")) || [];

    saved.forEach((func, index) => {

        let row = `
                                <tr>
                                    <td>${func}</td>
                                    <td>
                                        <button class="btn btn-danger btn-sm"
                                            onclick="deleteFunction(${index})">
                                            Delete
                                        </button>
                                    </td>
                                </tr>
                                `;

        table.innerHTML += row;
    });
}
function deleteFunction(index) {
    let saved = JSON.parse(localStorage.getItem("customFunctions")) || [];

    saved.splice(index, 1);
    localStorage.setItem("customFunctions", JSON.stringify(saved));

    renderFunctionTable();
    reloadDropdown();
}
function reloadDropdown() {
    let dropdown = document.getElementById("func");

    // Keep default options
    dropdown.innerHTML = `
    <option value="t/2 + t^2/3">
        t/2 + t²/3
    </option>

    <option value="t/2 + t^2/3 + t^3/4">
        t/2 + t²/3 + t³/4
    </option>

    <option value="t/3 + t^2/4 + t^3/5">
        t/3 + t²/4 + t³/5
    </option>
`;

    let saved = JSON.parse(localStorage.getItem("customFunctions")) || [];

    saved.forEach(func => {
        addFunctionToDropdown(func);
    });
}

// Download results as Excel >>>
async function downloadResultsExcel() {

    let data = {

        a1: document.getElementById("a1")?.value || "",
        k1: document.getElementById("k1")?.value || "",
        b1: document.getElementById("b1")?.value || "",
        f1: document.getElementById("f1")?.value || "",

        a2: document.getElementById("a2")?.value || "",
        k2: document.getElementById("k2")?.value || "",
        b2: document.getElementById("b2")?.value || "",
        f2: document.getElementById("f2")?.value || "",

        a3: document.getElementById("a3")?.value || "",
        k3: document.getElementById("k3")?.value || "",
        b3: document.getElementById("b3")?.value || "",
        f3: document.getElementById("f3")?.value || "",

        a4: document.getElementById("a4")?.value || "",
        k4: document.getElementById("k4")?.value || "",
        b4: document.getElementById("b4")?.value || "",
        f4: document.getElementById("f4")?.value || "",

        ta: document.getElementById("ta")?.value || "",
        tk: document.getElementById("tk")?.value || "",
        tb: document.getElementById("tb")?.value || "",
        ft: document.getElementById("ft")?.value || "",

        total: document.getElementById("total")?.value || "",
        gripper_name: document.getElementById("gripper") ?.selectedOptions[0]?.text || "",

        shape_name: document.getElementById("shape") ?.selectedOptions[0]?.text || "",

        material: document.getElementById("material")?.selectedOptions[0]?.text || "",

        time: document.getElementById("time").value,

        func: document.getElementById("func")?.selectedOptions[0]?.text || "",

        mode_name: document.querySelector('input[name="kmode"]:checked')
           ?.nextSibling?.textContent.trim() || "",
    };

    console.log(data);

    let response = await fetch("/download_excel", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(data)
    });

    if (!response.ok) {

        alert("Excel download failed");

        return;
    }

    let blob = await response.blob();

    let url = window.URL.createObjectURL(blob);

    let a = document.createElement("a");

    a.href = url;

    a.download = "gripper_results.xlsx";

    document.body.appendChild(a);

    a.click();

    a.remove();

    window.URL.revokeObjectURL(url);
}

