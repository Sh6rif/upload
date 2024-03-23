const express = require("express");
const { PythonShell } = require("python-shell");
const bodyParser = require("body-parser");
const cors = require("cors");
const fs = require("fs");
const path = require("path");
const app = express();
const port = 5000;

// Middleware setup
app.use(cors());
app.use(bodyParser.json({ limit: "50mb" }));
app.use(express.json());
app.set("view engine", "ejs");

// Root route
app.get("/", (req, res) => {
  res.render("img-process.ejs");
});

app.post("/upload", async (req, res) => {
  const imageData = req.body.image.replace(/^data:image\/\w+;base64,/, "");
  try {
    // Write image data to a temporary file
    const imagePath = path.join("temp_image.jpg");
    fs.writeFileSync(imagePath, imageData, "base64");
    PythonShell.run(
      "photo-string.py",
      { args: [imagePath] }, // Pass the path of the temporary file
      function (err, result) {
        if (err) {
          console.error(err);
          res.status(500).json({ error: "Failed to process image" });
        } else {
          res.json({ img: result[0], text: result[1] });
        }

        // Delete the temporary file after processing
        fs.unlinkSync(imagePath);
      }
    );
  } catch (error) {
    console.error("Error processing image:", error);
    res.status(500).json({ error: "Failed to process image" });
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
