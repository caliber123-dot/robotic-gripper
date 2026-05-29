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
    // if (f1 && d1) {
    //     funcStr += `${f1}/${d1}`;
    // }
    // TERM 1
    let op0 = document.getElementById("operator0").value;

    if (f1 && d1) {

        // negative first term
        if (op0 === "-") {
            funcStr += `-${f1}/${d1}`;
        }
        // positive first term
        else {
            funcStr += `${f1}/${d1}`;
        }
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
    // Clean localStorage.getItem("pno");
    // localStorage.removeItem("pno");
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

    let disposition =
    response.headers.get(
        "Content-Disposition"
    );

    let filename =
        "gripper_results.xlsx";

    if (
        disposition &&
        disposition.includes("filename=")
    ) {

        filename =
            disposition
                .split("filename=")[1]
                .replace(/"/g, "");
    }

    a.download = filename;

    document.body.appendChild(a);

    a.click();

    a.remove();

    window.URL.revokeObjectURL(url);
}

async function downloadResultsPdf() {

    let total = document.getElementById("total").value;

    // VALIDATION
    if (
        total === "" ||
        total === "0"
    ) {

        alert("Please calculate force first.");

        return;
    }

    let gripper =
        document.getElementById("gripper").value;

    let mode =
        document.querySelector(
            'input[name="kmode"]:checked'
        ).value;

    let mode_name = "";

    if (mode == "1") {

        mode_name = "All equal";
    }
    else if (mode == "2") {

        mode_name =
            "Fingers same, Thumb different";
    }
    else {

        mode_name = "All unequal";
    }

    let payload = {

        gripper_name:
            (gripper == "1")
                ? "4 Fingers"
                : "3 Fingers + 1 Thumb",

        shape_name:
            document.getElementById("shape")
                .options[
                document.getElementById("shape")
                    .selectedIndex
            ].text,

        material:
            document.getElementById("material")
                .options[
                document.getElementById("material")
                    .selectedIndex
            ].text,

        time:
            document.getElementById("time")
                .value,

        func:
            document.getElementById("func")
                .value,

        mode_name: mode_name,

        a1: document.getElementById("a1").value,
        a2: document.getElementById("a2").value,
        a3: document.getElementById("a3").value,
        a4: document.getElementById("a4").value,

        b1: document.getElementById("b1").value,
        b2: document.getElementById("b2").value,
        b3: document.getElementById("b3").value,
        b4: document.getElementById("b4").value,

        k1: document.getElementById("k1").value,
        k2: document.getElementById("k2").value,
        k3: document.getElementById("k3").value,
        k4: document.getElementById("k4").value,

        f1: document.getElementById("f1").value,
        f2: document.getElementById("f2").value,
        f3: document.getElementById("f3").value,
        f4: document.getElementById("f4").value,

        ta: document.getElementById("ta").value,
        tb: document.getElementById("tb").value,
        tk: document.getElementById("tk").value,
        ft: document.getElementById("ft").value,

        total: total
    };

    let response = await fetch(
        "/download_results_pdf",
        {

            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify(payload)

        }
    );

    let blob = await response.blob();

    let url =
        window.URL.createObjectURL(blob);

    let a =
        document.createElement("a");

    a.href = url;

    let disposition =
    response.headers.get(
        "Content-Disposition"
    );

    let filename =
        "gripper_results.pdf";

    if (
        disposition &&
        disposition.includes("filename=")
    ) {

        filename =
            disposition
                .split("filename=")[1]
                .replace(/"/g, "");
    }

    a.download = filename;

    a.click();
}

function clearSpringInputs(){

    let ids = [

        "k_common",
        "k_finger",

        "f1k1", "f1k2",
        "f2k1", "f2k2",
        "f3k1", "f3k2",
        "f4k1", "f4k2",

        "Thk1", "Thk2", "Thk3",
        "k_thumb",
        "k_thumb2",
        "k_thumb3"
    ];

    ids.forEach(id => {

        let el = document.getElementById(id);

        if(el){

            el.value = "";
        }
    });
}

function clearTable(){

    let ids = [

        "txtvolume",
        "txtmass",
        // A values
        "a10", "a1",
        "a20", "a2",
        "a30", "a3",
        "a40", "a4",
        "a50", "ta",

        // B values
        "b10", "b1",
        "b20", "b2",
        "b30", "b3",
        "b40", "b4",
        "b50", "tb",

        // K values
        "k1",
        "k2",
        "k3",
        "k4",
        "tk",

        // Force values
        "f1",
        "f2",
        "f3",
        "f4",
        "ft",

        // Total
        "total"

        // Execution time
        // "executionTime",
        // "executionTime2"
    ];

    ids.forEach(id => {

        let el =
            document.getElementById(id);

        if(el){

            // input textbox
            if(
                el.tagName === "INPUT" ||
                el.tagName === "TEXTAREA"
            ){

                el.value = "";
            }

            // normal div/span
            else{

                el.innerHTML = "";
            }
        }
    });
    document.getElementById("executionTime").innerHTML = "0";
    document.getElementById("executionTime2").innerHTML = "0";

}

async function getSavedData() {

    let gripper = getCurrentGripper();
    let shape =
        document.getElementById("shape").value;

    let material =
        document.getElementById("material").value;

    let time =
        document.getElementById("time").value;

    let func =
        document.getElementById("func").value;

    let mode =
        document.querySelector(
            'input[name="kmode"]:checked'
        ).value;

    // validation
    if (!shape || !material || !time || !func || !mode) {

        clearSpringInputs();

        return;
    }

    let response = await fetch(
        "/get_saved_data",
        {

            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({
                gripper: gripper,
                shape: shape,
                material: material,
                time: time,
                func: func,
                mode: mode
            })
        }
    );

    let result =
        await response.json();

    console.log(result);

    // =========================
    // FOUND
    // =========================

    if (result.status === "found") {

        let d = result.data;

        console.log(
            "Previous Data:",
            d
        );

        // avoid reload same data
        let currentTotal =
            document
            .getElementById("savedText")
            .getAttribute("data-total");

        if (currentTotal == d.total_force) {

            console.log(
                "Already loaded"
            );

            return;
        }

        // =========================
        // MODE 1
        // =========================

        let kCommon =
            document.getElementById(
                "k_common"
            );

        if (
            kCommon &&
            d.k_common != null
        ) {

            kCommon.value =
                d.k_common;
        }

        // =========================
        // MODE 2
        // =========================

        let kFinger =
            document.getElementById(
                "k_finger"
            );

        if (
            kFinger &&
            d.k_finger != null
        ) {

            kFinger.value =
                d.k_finger;
        }

        // =========================
        // ALL SPRING VALUES
        // =========================

        let mapValues = [

            ["f1k1", d.f1k1],
            ["f1k2", d.f1k2],

            ["f2k1", d.f2k1],
            ["f2k2", d.f2k2],

            ["f3k1", d.f3k1],
            ["f3k2", d.f3k2],

            ["f4k1", d.f4k1],
            ["f4k2", d.f4k2],

            ["Thk1", d.thk1],
            ["Thk2", d.thk2],
            ["Thk3", d.thk3],

            ["k_thumb", d.thk1],
            ["k_thumb2", d.thk2],
            ["k_thumb3", d.thk3]
        ];

        mapValues.forEach(item => {

            let id = item[0];

            let value = item[1];

            let el =
                document.getElementById(id);

            if (
                el &&
                value != null
            ) {

                el.value = value;
            }
        });

        // document.getElementById("isSaved").value = "1";
        await calculate(2);
        // alert("After calculation loaded");        
        // =========================
        // MESSAGE
        // =========================
        let total = document.getElementById("total").value;
        document.getElementById(
            "savedText"
        ).innerHTML =

        `
        <span class="text-success">
            <i class="bi bi-check-circle-fill"></i>
            Previous calculation loaded
        </span>

        <br>

        Total Force:
        <b>${total}</b>
        `;

        // cache current
        document
        .getElementById("savedText")
        .setAttribute(
            "data-total",
            total
        );
    }

    // =========================
    // NOT FOUND
    // =========================

    else {
        // document.getElementById("isSaved").value = "0";
        clearSpringInputs();
        //clear o/p table        
        clearTable();
        document
        .getElementById("savedText")
        .removeAttribute(
            "data-total"
        );
        // document.getElementById("savedText").style.display = "block";
        document.getElementById(
            "savedText"
        ).innerHTML =

        `
        <span class="text-danger">
            <i class="bi bi-exclamation-circle-fill"></i>
            No previous calculation found
        </span>
        `;
    }
}

document.getElementById("shape")
    .addEventListener("change", getSavedData);

document.getElementById("material")
    .addEventListener("change", getSavedData);

document.getElementById("time")
    .addEventListener("input", getSavedData);

document.getElementById("func")
    .addEventListener("change", getSavedData);

document
.querySelectorAll('input[name="kmode"]')
.forEach(radio => {

    radio.addEventListener(
        "change",
        getSavedData
    );

});

async function GetShapes() {

    let loader = document.getElementById("loader");
    let shape = +document.getElementById("shape").value;

    let event = "";
    let Rmajor = document.getElementById("Rmajor").value;
    let Rminor = document.getElementById("Rminor").value;

    let length = document.getElementById("length").value;
    let breadth = document.getElementById("breadth").value;
    let width = document.getElementById("width").value;

    let radius = document.getElementById("radius").value;

    if (!shape) {
        console.log("Shape not selected");
        // alert("Please select a shape");
        // markInvalid("shape");
        return false;
    }
    // 🔥 SHOW LOADER
    loader.style.display = "inline-block";
    // 🔥 GET SELECTION EVENT    

    if (shape == "3") { // Ellipsoidal
        if (document.getElementById("rbmajor").checked) {
            event = "major";
        } else if (document.getElementById("rbminor").checked) {
            event = "minor";
        }
        if (!Rmajor) {
            // markInvalid("Rmajor");
            return false;
        }
        if (!Rminor) {
            // markInvalid("Rminor");
            return false;
        }
    }
    else if (shape == "1") { // Rectangular
        if (document.getElementById("rblength").checked) {
            event = "length";
        } else if (document.getElementById("rbbreadth").checked) {
            event = "breadth";
        }
        if (!length) {
            // markInvalid("length");
            return false;
        }
        if (!breadth) {
            // markInvalid("breadth");
            return false;
        }
        if (!width) {
            // markInvalid("width");
            return false;
        }
        // alert("Event: " + event);
    }
    else if (shape == 2) { // Spherical
        event = "none"; // spherical doesn't have selection events      
        if (!radius) {
            // markInvalid("radius");
            return false;
        }
    }

    let data = {
        shape: +shape,
        event: event,
        Rmajor: Rmajor,
        Rminor: Rminor,
        length: length,
        breadth: breadth,
        width: width,
        radius: radius
    };
    let res = await fetch("/GetShapes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    let result = await res.json();
    // console.log(result);
    // ✅ Hide loader
    loader.style.display = "none";

    let gripper = getCurrentGripper();

    if (gripper == 1) {
        // document.getElementById("fig1").src = result.fig1;
        // document.getElementById("fig2").src = result.fig2;
        document.getElementById("fig2").src = result.fig2 + "?t=" + Date.now();
        // document.getElementById("fig3").src = result.fig3;
        // fig3D for figure 2
        document.getElementById("fig3d").src = result.fig3d + "?t=" + Date.now();
        document.getElementById("shape_name").innerText = result.shape_name;
    }
    else if (gripper == 2) {
        // document.getElementById("fig11").src = result.fig1;
        // document.getElementById("fig22").src = result.fig2;
        document.getElementById("fig22").src = result.fig2 + "?t=" + Date.now();
        // fig3D2 for figure 2
        document.getElementById("fig3d2").src = result.fig3d + "?t=" + Date.now();
        document.getElementById("shape_name2").innerText = result.shape_name;
    }
}