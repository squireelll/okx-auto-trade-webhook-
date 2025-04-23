const express = require("express");
const axios = require("axios");
const app = express();

app.use(express.json());

app.post("/", async (req, res) => {
  try {
    console.log("收到捷徑資料：", req.body);

    // 改成你的 Replit webhook（例如 http://localhost:8080/webhook）
    const response = await axios.post("http://localhost:8080/webhook", req.body, {
      timeout: 5000,
    });

    res.json({ status: "轉送成功", replitResponse: response.data });
  } catch (error) {
    console.error("轉送失敗：", error.message);
    res.status(500).json({ error: "轉送失敗", detail: error.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Proxy 啟動於 http://localhost:${PORT}`);
});
