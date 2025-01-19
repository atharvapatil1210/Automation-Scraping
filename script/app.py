const express = require("express");
const { exec } = require("child_process");
const path = require("path");
const app = express();
const port = 3000;

// Serve static files from the "public" directory (for the GUI)
app.use(express.static(path.join(__dirname, "public")));

// API route to run the Python scraper
app.get("/run-scraper", (req, res) => {
  exec("python3 index.py", (err, stdout, stderr) => {
    if (err) {
      console.error(`exec error: ${err}`);
      return res.status(500).send("Error running scraper");
    }
    if (stderr) {
      console.error(`stderr: ${stderr}`);
      return res.status(500).send("Error with Python script");
    }
    // Send the output of the Python script to the frontend
    res.send(stdout);
  });
});

// Home route to serve the main UI (HTML file)
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.listen(port, () => {
  console.log(`Express server running on http://localhost:${port}`);
});
