import { initializeApp } from "https://www.gstatic.com/firebasejs/11.1.0/firebase-app.js";
import { getDatabase, ref, get, child, push, set } from "https://www.gstatic.com/firebasejs/11.1.0/firebase-database.js";

// Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyCVPBxgQgt21CrGfoyFn7XybEVGpdZQjEs",
    authDomain: "sliding-puzzle-3ee47.firebaseapp.com",
    databaseURL: "https://sliding-puzzle-3ee47-default-rtdb.firebaseio.com",
    projectId: "sliding-puzzle-3ee47",
    storageBucket: "sliding-puzzle-3ee47.firebasestorage.app",
    messagingSenderId: "556260361773",
    appId: "1:556260361773:web:74e90587623b422fc5daa4",
    measurementId: "G-S06WLZCGDY"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Database
const database = getDatabase(app);


function writeData(path, in_name, in_move, in_best) {
    const dataRef = ref(database, path);
    const newPostRef = push(dataRef); 

    const data = {name: in_name, move: in_move, best: in_best}
    set(newPostRef, data)
        .then(() => {
            console.log(data);
            console.log("Data written successfully!");
        })
        .catch((error) => {
            console.error("Error writing data:", error);
        });
}

function readAndDisplayData(path) {
    const dbRef = ref(database, path);
    get(child(dbRef, "/"))
        .then((snapshot) => {
            if (snapshot.exists()) {
                const data = snapshot.val();
                console.log("Data read successfully:", data);

                // Convert data to an array and sort by "move"
                const sortedData = Object.values(data).sort((a, b) => a.move - b.move).slice(0, 100);
                // const sortedData = Object.values(data).sort((a, b) => (a.move - a.best) - (b.move - b.best)).slice(0, 100);

                
                // Update the table with sorted data
                updateRankingTable(sortedData);
            } else {
                console.log("No data available at the specified path.");
            }
        })
        .catch((error) => {
            console.error("Error reading data:", error);
        });
}


function updateRankingTable(sorteddata) {
    // Get the table body element
    const tableBody = document.getElementById("ranking-table").getElementsByTagName("tbody")[0];
    if (!tableBody) {
        console.error("Error: tbody element not found!");
        return;
    }

    // Check if sorteddata is valid
    if (!Array.isArray(sorteddata) || sorteddata.length === 0) {
        console.error("Error: Invalid or empty data provided!");
        tableBody.innerHTML = "<tr><td colspan='4'>No data available</td></tr>";
        return;
    }

    // Clear the table body before adding new rows
    tableBody.innerHTML = "";

    // Populate the table with sorted data
    sorteddata.forEach((item, index) => {
        const row = tableBody.insertRow();

        // Use default values if any field is missing
        const name = item.name || "Unknown";
        const move = item.move !== undefined ? item.move : "N/A";
        const best = item.best !== undefined ? item.best : "N/A";

        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${name}</td>
            <td>${move}</td>
            <td>${best}</td>
        `;
    });
}

const postData = [
    { name: "哈哈哈哈", move: 20, best: 15 },
    { name: "Andy", move: 54, best: 20 },
    { name: "Beth", move: 41, best: 21 },
    { name: "Jay Shih", move: -1, best: -1}
];

// postData.forEach((data) => writeData("data", data.name, data.move, data.best));
readAndDisplayData("data");
window.writeData = writeData;
window.readAndDisplayData = readAndDisplayData;