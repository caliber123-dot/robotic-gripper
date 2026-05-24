
Chart.register(ChartDataLabels);

// ===== THEME SYSTEM =====
let savedTheme = localStorage.getItem("selectedTheme");
let savedColor = localStorage.getItem("selectedTheme2");
if (savedTheme) {
    localStorage.removeItem("selectedTheme2");
    document.body.style.backgroundColor = ""; // clear inline color 
    document.body.className = savedTheme;
}
else if (savedColor) {
    localStorage.removeItem("selectedTheme");
    document.body.className = ""; // remove theme class
    document.body.style.backgroundColor = savedColor;
}
else {
    document.body.className = "theme-light";
}

function changeBackground() {
    let selectedColor = document.getElementById("startColor").value;
    document.body.style.backgroundColor = selectedColor;
    localStorage.setItem("selectedTheme2", selectedColor);
}
function previewTheme(theme) {
    document.body.className = theme;
}

function setTheme(theme) {
    document.body.className = theme;
    localStorage.setItem("selectedTheme", theme);
}

document
    .querySelector(".dropdown-menu")
    .addEventListener("mouseleave", function () {
        document.body.className =
            localStorage.getItem("selectedTheme") || "theme-light";
    });

// ===== MATERIAL DENSITY =====
const materials = { rubber: 1100, abs: 1040, teflon: 2200 };
function showhidewindow(pno) {

    let gripper = pno;
    let gripper_window = document.getElementById("gripper_window");

    let fig1 = document.getElementById("fig1");

    let txttime1 = document.getElementById("txttime1");
    let txtforce1 = document.getElementById("txtforce1");

    let length = document.getElementById("length");
    let breadth = document.getElementById("breadth");
    let width = document.getElementById("width");
    let radius = document.getElementById("radius");
    let Rmajor = document.getElementById("Rmajor");
    let Rminor = document.getElementById("Rminor");
    // let time = document.getElementById("time");
    let k_common = document.getElementById("k_common");
    let k_finger = document.getElementById("k_finger");
    let k_thumb = document.getElementById("k_thumb");
    let k_thumb2 = document.getElementById("k_thumb2");
    let k_thumb3 = document.getElementById("k_thumb3");
    let f1k1 = document.getElementById("f1k1");
    let f1k2 = document.getElementById("f1k2");
    let f2k1 = document.getElementById("f2k1");
    let f2k2 = document.getElementById("f2k2");
    let f3k1 = document.getElementById("f3k1");
    let f3k2 = document.getElementById("f3k2");
    let f4k1 = document.getElementById("f4k1");
    let f4k2 = document.getElementById("f4k2");
    let Thk1 = document.getElementById("Thk1");
    let Thk2 = document.getElementById("Thk2");
    let Thk3 = document.getElementById("Thk3");

    length.value = "100";
    breadth.value = "40";
    width.value = "20";
    radius.value = "50";
    Rmajor.value = "50";
    Rminor.value = "30";
    // let time = document.getElementById("time");
    k_common.value = "";
    k_finger.value = "";
    k_thumb.value = "";
    k_thumb2.value = "";
    k_thumb3.value = "";
    f1k1.value = "";
    f1k2.value = "";
    f2k1.value = "";
    f2k2.value = "";
    f3k1.value = "";
    f3k2.value = "";
    f4k1.value = "";
    f4k2.value = "";
    Thk1.value = "";
    Thk2.value = "";
    Thk3.value = "";

    // ================= TABLE =================

    document.getElementById(
        "graphTableBody"
    ).innerHTML = `

        <tr>
            <td>1 sec</td>
            <td>-</td>
        </tr>

        <tr>
            <td>2 sec</td>
            <td>-</td>
        </tr>

        <tr>
            <td>3 sec</td>
            <td>-</td>
        </tr>

        <tr>
            <td>4 sec</td>
            <td>-</td>
        </tr>

        <tr>
            <td>5 sec</td>
            <td>-</td>
        </tr>

    `;
    // ================= CHART =================

    if (forceChart) {

        forceChart.destroy();

        forceChart = null;
    }

    // clear canvas
    let canvas =
        document.getElementById("forceChart");

    let ctx = canvas.getContext("2d");

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    document.getElementById("shape_name").innerText = "-";
    fig1.src = "static/img/basic.avif";
    // alert("You have selected Gripper Type " + gripper + ". Click OK to proceed.");
    if (gripper == "") {
        gripper_window.setAttribute("data-title", "-");
        gripper_window.style.display = "none";

    }
    else if (gripper == 1) {
        gripper_window.setAttribute("data-title", "4 Fingers Graph");
        gripper_window.style.display = "block";
        // trFinger4.style.display = "table-row";
        document.getElementById("shape_name").innerText = "4 Fingers";

    }
    else if (gripper == 2) {
        gripper_window.setAttribute("data-title", "3 Fingers + 1 Thumb Graph");
        gripper_window.style.display = "block";
        // trFinger4.style.display = "none";
        document.getElementById("shape_name").innerText = "3 Fingers + 1 Thumb";

    }
    updateSpringFields();
}

function updateSpringFields() {
    // alert("Update spring fields called");
    console.log("Updating spring fields...");
    let gripper = sessionStorage.getItem("pno");
    let mode = document.querySelector('input[name="kmode"]:checked').value;
    // let container = document.getElementById("springInputs");
    let equal = document.getElementById("springInputs_equal");
    let samefinger = document.getElementById("springInputs_samefinger");
    let unequal = document.getElementById("springInputs_unequal");
    let msg = document.getElementById("springInputs_msg");

    let fingerCount = gripper == 1 ? 4 : 3;

    if (mode == 1) {
        equal.style.display = "block";
        samefinger.style.display = "none";
        unequal.style.display = "none";
        msg.style.display = "none";
    }

    if (mode == 2) {

        if (gripper == 2) {
            equal.style.display = "none";
            samefinger.style.display = "block";
            unequal.style.display = "none";
            msg.style.display = "none";
        }
        else {
            equal.style.display = "none";
            samefinger.style.display = "none";
            unequal.style.display = "none";
            msg.style.display = "block";
            msg.innerHTML = "Alert, Select Gripper Type : 3 Fingers + 1 Thumb"
        }

    }
    console.log("Mode:", mode, "Gripper:", gripper);
    if (mode == 3) {
        equal.style.display = "none";
        samefinger.style.display = "none";
        unequal.style.display = "block";
        msg.style.display = "none";
        let div_Finger4 = document.getElementById("div_Finger4");
        let div_Thumb = document.getElementById("div_Thumb");
        if (gripper == 2) {
            div_Thumb.style.display = "block";
            div_Finger4.style.display = "none";
        }
        else {
            div_Finger4.style.display = "block";
            div_Thumb.style.display = "none";
        }
    }
}

async function autoLoadSavedSpring() {

    let shape =
        document.getElementById(
            "shape"
        ).value;

    let material =
        document.getElementById(
            "material"
        ).value;

    let func =
        document.getElementById(
            "func"
        ).value;

    let mode =
        document.querySelector(
            'input[name="kmode"]:checked'
        )?.value;

    // fixed graph page time
    let time = 1;

    // validation
    if (
        !shape ||
        !material ||
        !func ||
        !mode
    ) {

        clearSpringInputs();

        return;
    }

    let response =
        await fetch(
            "/get_saved_data",
            {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

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
        
        clearSpringInputs();

        let d = result.data;

        console.log(
            "Auto loaded:",
            d
        );
        document.getElementById(
            "savedText"
        ).innerHTML =

            `
            <span class="text-success">
                <i class="bi bi-check-circle-fill"></i>
                Previous spring data loaded
            </span>
            `;

        // MODE 1
        if (
            d.k_common != null
        ) {

            let el =
                document.getElementById(
                    "k_common"
                );

            if (el) {

                el.value =
                    d.k_common;
            }
        }

        // MODE 2
        if (
            d.k_finger != null
        ) {

            let el =
                document.getElementById(
                    "k_finger"
                );

            if (el) {

                el.value =
                    d.k_finger;
            }
        }

        // MODE 2 THUMB
        let thumbs = [

            ["k_thumb", d.thk1],
            ["k_thumb2", d.thk2],
            ["k_thumb3", d.thk3]
        ];

        thumbs.forEach(item => {

            let el =
                document.getElementById(
                    item[0]
                );

            if (
                el &&
                item[1] != null
            ) {

                el.value =
                    item[1];
            }
        });

        // MODE 3
        let values = [

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
            ["Thk3", d.thk3]
        ];

        values.forEach(item => {

            let el =
                document.getElementById(
                    item[0]
                );

            if (
                el &&
                item[1] != null
            ) {

                el.value =
                    item[1];
            }
        });
    }

    // =========================
    // NOT FOUND
    // =========================

    else {

        // clearSpringInputs();
        clearSpringInputs();

        console.warn(
            "No saved spring data"
        );
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

function clearSpringInputs() {
    // executionTime and executionTime2
    document.getElementById("executionTime").innerText = "0";
    document.getElementById("executionTime2").innerText = "0";

    let ids = [

        "k_common",
        "k_finger",

        "k_thumb",
        "k_thumb2",
        "k_thumb3",

        "f1k1",
        "f1k2",

        "f2k1",
        "f2k2",

        "f3k1",
        "f3k2",

        "f4k1",
        "f4k2",

        "Thk1",
        "Thk2",
        "Thk3"
    ];

    ids.forEach(id => {

        let el =
            document.getElementById(id);

        if (el) {

            el.value = "";
        }
    });

    // =========================
    // CLEAR TABLE
    // =========================

    let tbody =
        document.getElementById(
            "graphTableBody"
        );

    if (tbody) {

        tbody.innerHTML = `

            <tr>
                <td>1 sec</td>
                <td>-</td>
            </tr>

            <tr>
                <td>2 sec</td>
                <td>-</td>
            </tr>

            <tr>
                <td>3 sec</td>
                <td>-</td>
            </tr>

            <tr>
                <td>4 sec</td>
                <td>-</td>
            </tr>

            <tr>
                <td>5 sec</td>
                <td>-</td>
            </tr>

        `;
    }

    // =========================
    // CLEAR CHART
    // =========================

    if (forceChart) {

        forceChart.destroy();

        forceChart = null;
    }

    // =========================
    // CLEAR CANVAS
    // =========================

    let canvas =
        document.getElementById(
            "forceChart"
        );

    if (canvas) {

        let ctx =
            canvas.getContext("2d");

        ctx.clearRect(
            0,
            0,
            canvas.width,
            canvas.height
        );
    }
}

var modal = document.getElementById("myModal");
var myModalFun = document.getElementById("myModalFun");
var modalImg = document.getElementById("img01");
function onMyPopupFun(ctrl) {
    myModalFun.style.display = "block";
    document.getElementById("twoTerms").checked = true;
    toggleTerms(2);
}

function onMyPopup(ctrl) {
    modal.style.display = "block";
    modalImg.src = ctrl.src;
    modalImg.alt = ctrl.alt;
    // captionText.innerHTML = ctrl.alt;
}
var span = document.getElementsByClassName("close")[0];
var span2 = document.getElementsByClassName("close")[1];

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
    modal.style.display = "none";
}
span2.onclick = function () {
    myModalFun.style.display = "none";
}
updateSpringFields();

function toggleTerms(count) {

    let operator1 =
        document.getElementById(
            "operatorGroup1"
        );

    let term2 =
        document.getElementById("cfunc3")
            .closest(".eq-block");

    let thirdGroup =
        document.getElementById(
            "thirdTermGroup"
        );

    // =========================
    // 1 TERM
    // =========================

    if (count == 1) {

        operator1.style.display = "none";

        term2.style.display = "none";

        thirdGroup.style.display = "none";
    }

    // =========================
    // 2 TERMS
    // =========================

    else if (count == 2) {

        operator1.style.display = "flex";

        term2.style.display = "flex";

        thirdGroup.style.display = "none";
    }

    // =========================
    // 3 TERMS
    // =========================

    else {

        operator1.style.display = "flex";

        term2.style.display = "flex";

        thirdGroup.style.display = "inline-flex";
    }
}

/* default load */
// document.addEventListener(
//     "DOMContentLoaded",
//     function () {

//         document.getElementById( "oneTerm" ).checked = true;

//         toggleTerms(1);
//     }
// );


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
/* default load */
window.addEventListener("load", () => {

    document.getElementById("twoTerms").checked = true;

    toggleTerms(2);
    let saved = JSON.parse(localStorage.getItem("customFunctions")) || [];

    saved.forEach(func => {
        // addFunctionToDropdown(func);
        reloadDropdown();
        renderFunctionTable();
    });

});

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

const sections = document.querySelectorAll("section, div[id]");
const navLinks = document.querySelectorAll(".nav-link");

window.addEventListener("scroll", () => {
    let current = "";

    sections.forEach((sec) => {
        const sectionTop = sec.offsetTop - 80;
        if (pageYOffset >= sectionTop) {
            current = sec.getAttribute("id");
        }
    });

    // navLinks.forEach((link) => {
    //     link.classList.remove("active");
    //     if (link.getAttribute("href") === "#" + current) {
    //         link.classList.add("active");
    //     }
    // });
});

function updateSelectionEvent() {
    let shape = document.getElementById("shape").value;
    // let container = document.getElementById("selectionEvent");
    let ellipsEvent = document.getElementById("ellipsEvent");
    let rectangleEvent = document.getElementById("rectangleEvent");
    let rectangleInput = document.getElementById("rectangleInput");
    let ellipsInput = document.getElementById("ellipsInput");
    let sphericalInput = document.getElementById("sphericalInput");
    let selectevt = document.getElementById("selectevt");
    // container.innerHTML = "";
    // Hide all first
    ellipsEvent.style.display = "none";
    rectangleEvent.style.display = "none";
    rectangleInput.style.display = "none";
    ellipsInput.style.display = "none";
    sphericalInput.style.display = "none";
    // selectevt.style.display = "block";
    // Ellipsoidal → Major / Minor
    if (shape == 3) {
        // Ellipsoidal
        // ellipsEvent.style.display = "flex";
        ellipsEvent.querySelectorAll("input").forEach(input => input.checked = false);
        document.getElementById("rbmajor").checked = true; // default selection
        // ellipsInput.style.display = "flex";
    }
    // Rectangular → Length / Breadth
    else if (shape == 1) {
        // Rectangular
        // rectangleEvent.style.display = "flex";
        rectangleEvent.querySelectorAll("input").forEach(input => input.checked = false);
        document.getElementById("rblength").checked = true; // default selection
        // rectangleInput.style.display = "flex";
    }
    // Spherical
    else {
        // sphericalInput.style.display = "flex";
        selectevt.style.display = "none";
        // container.innerHTML = `<small class="text-muted">No selection required</small>`;
        // ellipsEvent.style.display = "none";
        // rectangleEvent.style.display = "none";
    }
}
updateSelectionEvent();

// =========================
// AUTO LOAD SAVED DATA
// =========================

document
    .getElementById("shape")
    .addEventListener(
        "change",
        autoLoadSavedSpring
    );

document
    .getElementById("material")
    .addEventListener(
        "change",
        autoLoadSavedSpring
    );

document
    .getElementById("func")
    .addEventListener(
        "change",
        autoLoadSavedSpring
    );

// radio buttons
document
    .querySelectorAll(
        'input[name="kmode"]'
    )
    .forEach(r => {

        r.addEventListener(
            "change",
            autoLoadSavedSpring
        );
    });

// ################# For Calculation Grapgh Page

function validateInputs() {
    // alert("Validating inputs...");
    let mode = document.querySelector('input[name="kmode"]:checked').value;
    let gripper = sessionStorage.getItem("pno");
    // let time = document.getElementById("time").value;
    let material = document.getElementById("material").value;
    // let trFinger4 = document.getElementById("trFinger4");
    // let trThumb = document.getElementById("trThumb");
    let shape = +document.getElementById("shape").value;
    if (gripper == "") {
        // markInvalid("gripper");
        alert("Select Gripper Type");
        return false;
    }
    if (gripper == "1") {
        //4 Fingers
        // trFinger4.style.display = "table-row";
        // trThumb.style.display = "none";

    }
    else if (gripper == "2") {
        // 3 Fingers + 1 Thumb
        // trFinger4.style.display = "none";
        // trThumb.style.display = "table-row";
    }
    // if Select Shape then validate shape parameters
    if (!shape) {
        markInvalid("shape");
        return false;
    }
    if (material == "") {
        markInvalid("material");
        return false;
    }
    if (shape == 1) {
        let length = document.getElementById("length").value;
        let breadth = document.getElementById("breadth").value;
        let width = document.getElementById("width").value;
        if (!length) {
            markInvalid("length");
            return false;
        }
        if (!breadth) {
            markInvalid("breadth");
            return false;
        }
        if (!width) {
            markInvalid("width");
            return false;
        }
    }
    else if (shape == 2) {
        let radius = document.getElementById("radius").value;
        if (!radius) {
            markInvalid("radius");
            return false;
        }
    }
    else if (shape == 3) {
        let Rmajor = document.getElementById("Rmajor").value;
        let Rminor = document.getElementById("Rminor").value;
        if (!Rmajor) {
            markInvalid("Rmajor");
            return false;
        }
        if (!Rminor) {
            markInvalid("Rminor");
            return false;
        }
    }
    // if (!time) {
    //     // alert("Please enter Time");
    //     markInvalid("time");
    //     return false;
    // }
    // alert("shape entered: " + shape);

    if (!material) {
        // alert("Please select Material");
        markInvalid("material");
        return false;
    }

    // Reset borders
    document.querySelectorAll("input").forEach(el => el.style.border = "");

    function invalid(id) {
        let el = document.getElementById(id);
        el.focus();
        if (el) el.style.border = "2px solid red";
    }

    // ===== MODE 1: ALL EQUAL =====
    if (mode == "1") {
        let k = document.getElementById("k_common").value;

        if (!k) {
            // invalid("k_common");
            markInvalid("k_common");
            // alert("Enter Common K");
            return false;
        }
    }

    // ===== MODE 2: FINGER SAME, THUMB DIFFERENT =====
    if (mode == "2") {
        let kf = document.getElementById("k_finger")?.value;
        let kt1 = document.getElementById("k_thumb")?.value;
        let kt2 = document.getElementById("k_thumb2")?.value;
        let kt3 = document.getElementById("k_thumb3")?.value;

        if (gripper == "2" && !kf) {
            // invalid("k_finger");
            markInvalid("k_finger");
            // alert("Enter Finger K");
            return false;
        }

        if (gripper == "2" && !kt1) {
            markInvalid("k_thumb");
            return false;
        }
        if (gripper == "2" && !kt2) {
            markInvalid("k_thumb2");
            return false;
        }
        if (gripper == "2" && !kt3) {
            markInvalid("k_thumb3");
            return false;
        }
    }

    // ===== MODE 3: ALL UNEQUAL =====
    if (mode == "3") {

        let fingerCount = (gripper == "1") ? 4 : 3;

        for (let i = 1; i <= fingerCount; i++) {

            let k1 = document.getElementById(`f${i}k1`)?.value;
            let k2 = document.getElementById(`f${i}k2`)?.value;

            if (!k1) {
                invalid(`f${i}k1`);
                // alert(`Enter Finger ${i} Spring 1`);
                return false;
            }

            if (!k2) {
                invalid(`f${i}k2`);
                // alert(`Enter Finger ${i} Spring 2`);
                return false;
            }
        }

        // Thumb (only if gripper = 3+1)
        if (gripper == "2") {
            let t1 = document.getElementById("Thk1")?.value;
            let t2 = document.getElementById("Thk2")?.value;
            let t3 = document.getElementById("Thk3")?.value;

            if (!t1) {
                invalid("Thk1");
                // alert("Enter Thumb K1"); 
                return false;
            }
            if (!t2) {
                invalid("Thk2");
                // alert("Enter Thumb K2"); 
                return false;
            }
            if (!t3) {
                invalid("Thk3");
                // alert("Enter Thumb K3"); 
                return false;
            }
        }
    }

    return true;
}
function markInvalid(id) {
    let el = document.getElementById(id);
    el.focus();
    el.style.border = "2px solid red";
}
// Main Logic to call backend and calculate forces
async function calculate() {
    console.log("✅ Working calculate function called");
    // 🔥 VALIDATION FIRST
    // alert("Validation started");
    if (!validateInputs()) return;
    console.log("Validation Passed ✅");
    let loader = document.getElementById("loader");
    let execTime = document.getElementById("executionTime");
    let execTime2 = document.getElementById("executionTime2");
    // 🔥 SHOW LOADER
    loader.style.display = "inline-block";
    execTime.innerText = "0";
    execTime2.innerText = "0";
    let shape = +document.getElementById("shape").value;

    // 🔥 GET SELECTION EVENT
    let event = "";

    if (shape == "3") { // Ellipsoidal
        if (document.getElementById("rbmajor").checked) {
            event = "major";
        } else if (document.getElementById("rbminor").checked) {
            event = "minor";
        }
    }
    else if (shape == "1") { // Rectangular
        if (document.getElementById("rblength").checked) {
            event = "length";
        } else if (document.getElementById("rbbreadth").checked) {
            event = "breadth";
        }
        // alert("Event: " + event);
    }
    else {
        event = "none"; // spherical
    }
    // if (!event) {
    //     alert("Please select Selection Event");
    //     return;
    // }
    let mode = document.querySelector('input[name="kmode"]:checked').value;
    let data = {
        shape: +shape,
        event: event,   // 🔥 SEND TO BACKEND
        length: +document.getElementById("length").value,
        breadth: +document.getElementById("breadth").value,
        width: +document.getElementById("width").value,
        radius: +document.getElementById("radius").value,
        Rmajor: +document.getElementById("Rmajor").value,
        Rminor: +document.getElementById("Rminor").value,
        material: document.getElementById("material").value,
        // time: +document.getElementById("time").value,
        // func: document.getElementById("func").value,
        func: document.getElementById("func").value,
        gripper: sessionStorage.getItem("pno"),
        mode: mode,
        k_common: +document.getElementById("k_common")?.value || 0,
        k_finger: +document.getElementById("k_finger")?.value || 0,
        thumb: (mode == "2")
            ? [
                +document.getElementById("k_thumb")?.value || 0,
                +document.getElementById("k_thumb2")?.value || 0,
                +document.getElementById("k_thumb3")?.value || 0
            ]
            : [
                +document.getElementById("Thk1")?.value || 0,
                +document.getElementById("Thk2")?.value || 0,
                +document.getElementById("Thk3")?.value || 0
            ],

        fingers: [
            { k1: +document.getElementById("f1k1")?.value || 0, k2: +document.getElementById("f1k2")?.value || 0 },
            { k1: +document.getElementById("f2k1")?.value || 0, k2: +document.getElementById("f2k2")?.value || 0 },
            { k1: +document.getElementById("f3k1")?.value || 0, k2: +document.getElementById("f3k2")?.value || 0 },
            { k1: +document.getElementById("f4k1")?.value || 0, k2: +document.getElementById("f4k2")?.value || 0 }
        ]
    };

    // let res = await fetch("/calculate_graph", {
    //     method: "POST",
    //     headers: { "Content-Type": "application/json" },
    //     body: JSON.stringify(data)
    // });

    // let result = await res.json();
    // ✅ Set Time & Force in 5 rows
    // document.getElementById("txttime1").value = result.time1?.toFixed(5) || "";
    // document.getElementById("txtforce1").value = result.force1?.toFixed(5) || "";
    // document.getElementById("txttime2").value = result.time2?.toFixed(5) || "";
    // document.getElementById("txtforce2").value = result.force2?.toFixed(5) || "";
    // document.getElementById("txttime3").value = result.time3?.toFixed(5) || "";
    // document.getElementById("txtforce3").value = result.force3?.toFixed(5) || "";
    // document.getElementById("txttime4").value = result.time4?.toFixed(5) || "";
    // document.getElementById("txtforce4").value = result.force4?.toFixed(5) || "";
    // document.getElementById("txttime5").value = result.time5?.toFixed(5) || "";
    // document.getElementById("txtforce5").value = result.force5?.toFixed(5) ||"";


    // ✅ Hide loader
    // loader.style.display = "block";
    // // ✅ Show execution time and Generate Graph Image (png) in fig1
    // execTime.innerText = result.execution_time;
    // let gripper = document.getElementById("gripper").value;
    // // alert("gripper: " + gripper + " mode: " + mode);
    // if (gripper == "1") {
    //     document.getElementById("fig1").src = result.fig1;

    // }
    // else if (gripper == "2") {
    //     document.getElementById("fig1").src = result.fig1;        
    // }
    // console.log("Fig1 URL:", result.fig1);

    // ================= TIME vs FORCE =================
    // ================= GRAPH API =================

    let graphResponse = await fetch("/calculate_graph", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(data)

    });

    let graphResult = await graphResponse.json();

    execTime.innerText = graphResult.execution_time;
    execTime2.innerText = (graphResult.execution_time / 1000).toFixed(4);
    loader.style.display = "none";

    createBarChart(
        graphResult.time,
        graphResult.force
    );

    updateGraphTable(
        graphResult.time,
        graphResult.force
    );

}

// ============================= New ===============
// ================= BAR CHART =================

// ================= BAR CHART =================

let forceChart = null;

function createBarChart(timeData, forceData) {

    const canvas =
        document.getElementById("forceChart");

    const ctx =
        canvas.getContext("2d");

    // destroy previous chart
    if (forceChart) {

        forceChart.destroy();
    }

    // IMPORTANT FIX
    setTimeout(() => {

        forceChart = new Chart(ctx, {

            type: "bar",

            data: {

                labels: timeData,

                datasets: [{

                    label: "Force",

                    data: forceData,

                    borderWidth: 2,

                    borderColor: "#000",

                    backgroundColor: [
                        "#4e79a7",
                        "#59a14f",
                        "#f28e2b",
                        "#e15759",
                        "#b07aa1"
                    ]
                }]
            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {
                        display: true
                    },

                    datalabels: {

                        anchor: "end",

                        align: "top",

                        color: "black",

                        font: {

                            weight: "bold",

                            size: 12
                        },

                        formatter: function (value) {

                            return Number(value)
                                .toLocaleString();
                        }
                    }
                },

                animation: {
                    duration: 1000
                },

                scales: {

                    x: {

                        title: {

                            display: true,

                            text: "Time (sec)",

                            color: "#444",

                            font: {
                                size: 16,
                                weight: "bold"
                            }
                        }
                    },

                    y: {

                        type: "logarithmic",
                        beginAtZero: true,

                        title: {

                            display: true,

                            text: "Force (N)",

                            color: "#444",

                            font: {
                                size: 16,
                                weight: "bold"
                            }
                        }
                    }
                }

            }
        });

    }, 200); // small render delay

    // save chart image
    setTimeout(() => {

        let chartBase64 =
            document
                .getElementById("forceChart")
                .toDataURL("image/png");

        document.getElementById("chartImage").value =
            chartBase64;

    }, 1000);
}

function updateGraphTable(timeData, forceData) {

    let tbody =
        document.getElementById("graphTableBody");

    tbody.innerHTML = "";

    for (let i = 0; i < timeData.length; i++) {

        tbody.innerHTML += `

            <tr>
                <td>${timeData[i]}</td>
                <td>${forceData[i]} (N)</td>
            </tr>

        `;
    }
}

async function downloadGraphExcel() {

    let tableRows =
        document.querySelectorAll("#graphTableBody tr");

    let tableData = [];

    tableRows.forEach(row => {

        let cols = row.querySelectorAll("td");

        let forceValue =
            cols[1].innerText.trim();

        // skip empty rows
        if (
            forceValue === "-" ||
            forceValue === ""
        ) {
            return;
        }

        tableData.push({

            time: cols[0].innerText,

            force: forceValue

        });

    });
    if (tableData.length === 0) {

        alert(
            "Please generate graph first."
        );

        return;
    }

    let payload = {

        func: document.getElementById("func").value,
        // alert("sss" + localStorage.getItem("pno") || "0")
        mode_name: document.querySelector('input[name="kmode"]:checked').value == "1"

            ? "All equal"

            : document.querySelector(
                'input[name="kmode"]:checked'
            ).value == "2"

                ? "Fingers same, Thumb different"

                : "All unequal",

        gripper_name:
            sessionStorage.getItem("pno") == 1

                ? "4 Fingers"

                : "3 Fingers + 1 Thumb",
        shape_name:
            document.getElementById("shape_name").innerText,

        object_shape:
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

        graphImage:
            document.getElementById("chartImage").value,

        tableData: tableData

    };

    let response = await fetch("/download_graph_excel", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(payload)

    });

    let blob = await response.blob();

    let url = window.URL.createObjectURL(blob);

    let a = document.createElement("a");

    a.href = url;

    // a.download = "Graph_Report.xlsx";
    let disposition =
        response.headers.get(
            "Content-Disposition"
        );

    let filename =
        "Graph_Report.xlsx";

    if (disposition &&
        disposition.includes("filename=")) {

        filename =
            disposition
                .split("filename=")[1]
                .replace(/"/g, "");
    }

    a.download = filename;

    a.click();
}

async function downloadGraphPdf() {

    let tableRows =
        document.querySelectorAll("#graphTableBody tr");

    let tableData = [];

    tableRows.forEach(row => {

        let cols = row.querySelectorAll("td");

        let forceValue =
            cols[1].innerText.trim();

        // skip empty rows
        if (
            forceValue === "-" ||
            forceValue === ""
        ) {
            return;
        }

        tableData.push({

            time: cols[0].innerText,

            force: forceValue

        });

    });

    // VALIDATION SAME AS EXCEL
    if (tableData.length === 0) {

        alert("Please generate graph first.");

        return;
    }

    let payload = {

        func:
            document.getElementById("func")
                .value,

        mode_name:
            document.querySelector(
                'input[name="kmode"]:checked'
            ).value == "1"

                ? "All equal"

                : document.querySelector(
                    'input[name="kmode"]:checked'
                ).value == "2"

                    ? "Fingers same, Thumb different"

                    : "All unequal",

        gripper_name:
            sessionStorage.getItem("pno") == 1

                ? "4 Fingers"

                : "3 Fingers + 1 Thumb",
        shape_name:
            document.getElementById("shape_name").innerText,

        object_shape:
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

        graphImage:
            document.getElementById("chartImage").value,

        tableData: tableData

    };

    let response = await fetch("/download_graph_pdf", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(payload)

    });

    let blob = await response.blob();

    let url = window.URL.createObjectURL(blob);

    let a = document.createElement("a");

    a.href = url;

    let disposition =
        response.headers.get(
            "Content-Disposition"
        );

    let filename =
        "Graph_Report.pdf";

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