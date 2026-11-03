const API_BASE_URL = "/api/v1";

const api = {
    async getPreview(fileId) {
        const res = await fetch(`${API_BASE_URL}/dataset/preview/${fileId}`);
        const data = await res.json();
        if (!res.ok) throw new Error(data.message || "Lỗi khi lấy dữ liệu preview");
        return data;
    },

    async uploadCSV(file) {
        const formData = new FormData();
        formData.append("file", file);
        const res = await fetch(`${API_BASE_URL}/dataset/upload`, {
            method: "POST",
            body: formData
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.message || "Lỗi khi tải file lên");
        return data;
    },

    async runElbowAnalysis(fileId, featureColumns, scalingMethod = "standard", maxK = 10) {
        const res = await fetch(`${API_BASE_URL}/analysis/elbow`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                file_id: fileId,
                feature_columns: featureColumns,
                scaling_method: scalingMethod,
                max_k: maxK
            })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.message || "Lỗi khi phân tích Elbow");
        return data;
    },

    async trainKMeans(fileId, featureColumns, nClusters, scalingMethod = "standard") {
        const res = await fetch(`${API_BASE_URL}/clustering/train`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                file_id: fileId,
                feature_columns: featureColumns,
                n_clusters: nClusters,
                scaling_method: scalingMethod
            })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.message || "Lỗi khi huấn luyện K-Means");
        return data;
    },

    async predictStudent(features) {
        const res = await fetch(`${API_BASE_URL}/predict`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ features })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.message || "Lỗi khi dự đoán sinh viên");
        return data;
    }
};
