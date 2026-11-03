let currentFileId = null;
let currentNumericColumns = [];
let selectedFeatures = [];

// Khởi chạy khi load trang
document.addEventListener("DOMContentLoaded", () => {
    setupEventListeners();
});

function setupEventListeners() {
    // 1. Nạp Dataset mẫu
    document.getElementById("btnLoadSample").addEventListener("click", async () => {
        try {
            const res = await api.getPreview("sample");
            handleDatasetLoaded("student_sample.csv", res.data);
        } catch (err) {
            alert("Lỗi: " + err.message);
        }
    });

    // 2. Upload file CSV
    document.getElementById("fileInput").addEventListener("change", async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        try {
            const res = await api.uploadCSV(file);
            handleDatasetLoaded(res.file_id, res.data);
        } catch (err) {
            alert("Lỗi tải file: " + err.message);
        }
    });

    // 3. Phân tích Elbow & Silhouette
    document.getElementById("btnRunElbow").addEventListener("click", async () => {
        updateSelectedFeatures();
        if (!currentFileId || selectedFeatures.length < 2) {
            alert("Vui lòng nạp dataset và chọn ít nhất 2 đặc trưng số!");
            return;
        }

        const scaling = document.getElementById("scalingMethod").value;
        try {
            const res = await api.runElbowAnalysis(currentFileId, selectedFeatures, scaling);
            document.getElementById("analysisCharts").classList.remove("hidden");
            charts.renderElbow(res.data.k_values, res.data.inertias);
            charts.renderSilhouette(res.data.k_values, res.data.silhouette_scores);
            
            // Gợi ý K tối ưu
            document.getElementById("inputK").value = res.data.recommended_k;
        } catch (err) {
            alert("Lỗi phân tích: " + err.message);
        }
    });

    // 4. Huấn luyện K-Means
    document.getElementById("btnTrainKMeans").addEventListener("click", async () => {
        updateSelectedFeatures();
        if (!currentFileId || selectedFeatures.length < 2) {
            alert("Vui lòng chọn ít nhất 2 đặc trưng số để phân cụm!");
            return;
        }

        const k = parseInt(document.getElementById("inputK").value);
        const scaling = document.getElementById("scalingMethod").value;

        try {
            const res = await api.trainKMeans(currentFileId, selectedFeatures, k, scaling);
            document.getElementById("clusteringResults").classList.remove("hidden");
            
            // Vẽ đồ thị PCA
            charts.renderPCA(res.data.pca_data, res.data.pca_centroids);
            
            // Render profiles
            renderClusterProfiles(res.data.profiles);

            // Render form dự đoán cho sinh viên mới
            renderPredictionForm(selectedFeatures);
        } catch (err) {
            alert("Lỗi huấn luyện K-Means: " + err.message);
        }
    });
}

function handleDatasetLoaded(fileId, data) {
    currentFileId = fileId;
    currentNumericColumns = data.numeric_columns.filter(c => c !== "student_id" && c !== "id");
    selectedFeatures = [...currentNumericColumns];

    // Hiển thị preview
    document.getElementById("datasetPreview").classList.remove("hidden");
    document.getElementById("previewFilename").innerText = `${fileId} (${data.total_rows} dòng, ${data.total_columns} cột)`;

    const tableHead = document.querySelector("#previewTable thead");
    const tableBody = document.querySelector("#previewTable tbody");
    
    tableHead.innerHTML = `<tr>${data.columns.map(c => `<th class="px-3 py-2">${c}</th>`).join("")}</tr>`;
    tableBody.innerHTML = data.sample_data.map(row => 
        `<tr class="hover:bg-slate-50">${data.columns.map(c => `<td class="px-3 py-1.5 border-t">${row[c] !== undefined ? row[c] : ""}</td>`).join("")}</tr>`
    ).join("");

    // Hiển thị danh sách checkbox chọn features
    const featureContainer = document.getElementById("featureList");
    featureContainer.innerHTML = currentNumericColumns.map(col => `
        <label class="inline-flex items-center gap-1.5 bg-slate-100 px-2.5 py-1 rounded-md border border-slate-200 cursor-pointer">
            <input type="checkbox" name="features" value="${col}" checked class="rounded text-indigo-600 focus:ring-indigo-500">
            <span>${col}</span>
        </label>
    `).join("");
}

function updateSelectedFeatures() {
    const checked = document.querySelectorAll('input[name="features"]:checked');
    selectedFeatures = Array.from(checked).map(cb => cb.value);
}

function renderClusterProfiles(profiles) {
    const container = document.getElementById("clusterProfilesGrid");
    container.innerHTML = profiles.map(p => `
        <div class="cluster-card bg-slate-50 border border-slate-200 rounded-lg p-4">
            <div class="flex justify-between items-center mb-2">
                <span class="font-bold text-indigo-700">Cụm ${p.cluster}</span>
                <span class="text-xs font-semibold bg-indigo-100 text-indigo-800 px-2 py-0.5 rounded-full">${p.count} SV (${p.percentage}%)</span>
            </div>
            <div class="space-y-1 text-xs text-slate-600">
                ${Object.entries(p.feature_means).map(([feat, mean]) => `
                    <div class="flex justify-between border-b border-slate-200 py-1">
                        <span class="font-medium">${feat}:</span>
                        <span class="font-bold text-slate-800">${mean}</span>
                    </div>
                `).join("")}
            </div>
        </div>
    `).join("");
}

function renderPredictionForm(features) {
    const container = document.getElementById("predictFormContainer");
    container.innerHTML = `
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
            ${features.map(f => `
                <div>
                    <label class="block text-xs font-semibold text-slate-600 mb-1">${f}:</label>
                    <input type="number" step="any" id="pred_${f}" placeholder="Nhập ${f}" class="w-full border border-slate-300 rounded-lg px-3 py-1.5 text-sm">
                </div>
            `).join("")}
        </div>
        <button id="btnSubmitPredict" class="mt-4 bg-emerald-600 hover:bg-emerald-700 text-white px-5 py-2 rounded-lg font-medium text-sm transition">
            🔮 Phân Cụm Sinh Viên & Giải Thích
        </button>
    `;

    document.getElementById("btnSubmitPredict").addEventListener("click", async () => {
        const payload = {};
        for (const f of features) {
            const val = document.getElementById(`pred_${f}`).value;
            if (val === "") {
                alert(`Vui lòng nhập giá trị cho ${f}`);
                return;
            }
            payload[f] = parseFloat(val);
        }

        try {
            const res = await api.predictStudent(payload);
            const resBox = document.getElementById("predictResult");
            resBox.classList.remove("hidden");
            resBox.innerHTML = `
                <div class="font-bold text-indigo-900 text-base mb-1">
                    📌 Kết quả: Xếp vào <span class="text-emerald-700 font-extrabold">${res.data.cluster_label}</span>
                </div>
                <p class="text-sm text-slate-700 mb-3">${res.data.explanation}</p>
                <div class="text-xs text-slate-600 bg-white p-3 rounded border border-indigo-100">
                    <span class="font-semibold block mb-1">Khoảng cách tới các tâm cụm:</span>
                    ${Object.entries(res.data.distances_to_centroids).map(([c, d]) => `<span class="mr-4">${c}: <b>${d}</b></span>`).join("")}
                </div>
            `;
        } catch (err) {
            alert("Lỗi dự đoán: " + err.message);
        }
    });
}
