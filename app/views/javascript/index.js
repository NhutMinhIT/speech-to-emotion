$(function () {
    // Tabs
    $(".tab-btn").on("click", function () {
        $(".tab-btn").removeClass("active bg-white/30").addClass("bg-white/20");
        $(this).addClass("active bg-white/30");
        $(".panel").addClass("hidden");
        $($(this).data("target")).removeClass("hidden");
    });

    // Upload
    let selectedFile = null;
    $("#audioFile").on("change", function (e) {
        selectedFile = e.target.files[0] || null;
        $("#btnUpload").prop("disabled", !selectedFile);
        if (selectedFile) {
            const url = URL.createObjectURL(selectedFile);
            $("#uploadAudioPreview").html(`<audio controls class="w-full" src="${url}"></audio>`);
        } else {
            $("#uploadAudioPreview").empty();
        }
    });

    $("#btnUpload").on("click", async function () {
        if (!selectedFile) return;
        const fd = new FormData();
        fd.append("file", selectedFile, selectedFile.name);
        $("#uploadResult").html(`<div class="rounded-xl bg-yellow-50 text-yellow-700 px-4 py-3">Đang phân tích...</div>`);
        try {
            const res = await fetch("/api/predict", { method: "POST", body: fd });
            const data = await res.json();
            if (data.success) {
                $("#uploadResult").html(
                    `<div class="rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-700 px-4 py-3">
             Cảm xúc: <b>${data.label}</b>
           </div>`
                );
            } else {
                $("#uploadResult").html(
                    `<div class="rounded-xl bg-rose-50 border border-rose-200 text-rose-700 px-4 py-3">
             Lỗi: ${data.detail || "Không xác định"}
           </div>`
                );
            }
        } catch (err) {
            $("#uploadResult").html(
                `<div class="rounded-xl bg-rose-50 border border-rose-200 text-rose-700 px-4 py-3">
           Lỗi: ${err}
         </div>`
            );
        }
    });

    // Recording
    let mediaRecorder, chunks = [];
    $("#btnStart").on("click", async function () {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        chunks = [];
        mediaRecorder.ondataavailable = e => { if (e.data.size > 0) chunks.push(e.data); };
        mediaRecorder.onstop = async () => {
            const blob = new Blob(chunks, { type: mediaRecorder.mimeType || "audio/webm" });
            const url = URL.createObjectURL(blob);
            $("#recordPreview").html(`<audio controls class="w-full" src="${url}"></audio>`);

            const fd = new FormData();
            fd.append("file", blob, "recorded.webm");
            $("#recordResult").html(`<div class="rounded-xl bg-yellow-50 text-yellow-700 px-4 py-3">Đang phân tích...</div>`);
            try {
                const res = await fetch("/api/predict", { method: "POST", body: fd });
                const data = await res.json();
                if (data.success) {
                    $("#recordResult").html(
                        `<div class="rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-700 px-4 py-3">
               Cảm xúc: <b>${data.label}</b>
             </div>`
                    );
                } else {
                    $("#recordResult").html(
                        `<div class="rounded-xl bg-rose-50 border border-rose-200 text-rose-700 px-4 py-3">
               Lỗi: ${data.detail || "Không xác định"}
             </div>`
                    );
                }
            } catch (err) {
                $("#recordResult").html(
                    `<div class="rounded-xl bg-rose-50 border border-rose-200 text-rose-700 px-4 py-3">
             Lỗi: ${err}
           </div>`
                );
            }
        };

        mediaRecorder.start();
        $("#btnStart").prop("disabled", true).addClass("opacity-60");
        $("#btnStop").prop("disabled", false).removeClass("opacity-60");
    });

    $("#btnStop").on("click", function () {
        if (mediaRecorder && mediaRecorder.state !== "inactive") {
            mediaRecorder.stop();
            $("#btnStart").prop("disabled", false).removeClass("opacity-60");
            $("#btnStop").prop("disabled", true).addClass("opacity-60");
        }
    });
});
