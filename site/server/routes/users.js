var express = require("express");
var router = express.Router();

const sqlite3 = require("sqlite3").verbose();
/* GET users listing. */
router.get("/rankings", (req, res) => {
  let db = new sqlite3.Database("../../data-collection/debate.db");
  const sql = `SELECT * FROM rankings WHERE name != '' AND school != ''`;
  db.all(sql, [], (err, rows) => {
    if (err) {
      console.log(err.message);
      console.log(err.stack);
      throw err;
    }
    // Only ranked if participated in at least 2 tournaments
    // TODO:

    rows.forEach((row, index) => (row.id = index + 1));
    res.json(rows);
  });
  db.close();
});

router.get("/all_debaters", (req, res) => {
  let db = new sqlite3.Database("../../data-collection/debate.db");
  const sql = `SELECT * FROM rankings WHERE name != '' AND school != ''`;
  db.all(sql, [], (err, rows) => {
    if (err) {
      console.log(err.message);
      console.log(err.stack);
      throw err;
    }
    rows.forEach((row, index) => (row.id = index + 1));
    res.json(rows);
  });
  db.close();
});

router.get("/get_rounds", (req, res) => {
  let db = new sqlite3.Database("../../data-collection/debate.db");
  let code = "";
  for (char of req.query.code) {
    code += char == "_" ? " " : char;
  }
  console.log(code);

  const sql = `SELECT * FROM rounds WHERE debater_a_code = $code OR debater_b_code = $code`;
  db.all(sql, [code], (err, rows) => {
    if (err) {
      console.log(err.message);
      console.log(err.stack);
      throw err;
    }
    res.json(rows);
  });
  db.close();
});

router.get("/get_debater", (req, res) => {
  let db = new sqlite3.Database("../../data-collection/debate.db");
  let code = "";
  for (char of req.query.code) {
    code += char == "_" ? " " : char;
  }
  console.log(code);

  const sql = `SELECT * FROM rankings WHERE code = $code LIMIT 1`;
  db.all(sql, [code], (err, rows) => {
    if (err) {
      console.log(err.message);
      console.log(err.stack);
      throw err;
    }
    console.log(rows);
    res.json(rows[0]);
  });
  db.close();
});

module.exports = router;
