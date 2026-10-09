import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import vm from "node:vm";

const root = resolve(import.meta.dirname, "..");
const requiredFiles = [
  "index.html",
  "styles.css",
  "js/app.js",
  "js/projects.js",
  "assets/mohith-dharshan.jpg",
  "assets/Mohith_Dharshan_Resume.pdf",
  "assets/favicon.svg",
  "site.webmanifest",
  "vercel.json"
];

for (const file of requiredFiles) {
  if (!existsSync(resolve(root, file))) throw new Error(`Missing required file: ${file}`);
}

const html = readFileSync(resolve(root, "index.html"), "utf8");
for (const id of ["main", "work", "academics", "repositories", "about", "contact", "project-dialog"]) {
  if (!html.includes(`id="${id}"`)) throw new Error(`Missing required page landmark: ${id}`);
}

for (const score of ["8.53", "9.16", "8.85"]) {
  if (!html.includes(score)) throw new Error(`Missing academic score: ${score}`);
}

const context = { window: {} };
vm.createContext(context);
vm.runInContext(readFileSync(resolve(root, "js/projects.js"), "utf8"), context);
const { featured, repositories } = context.window.PORTFOLIO_DATA;

if (featured.length !== 7) throw new Error(`Expected 7 featured projects, found ${featured.length}`);
if (repositories.length !== 31) throw new Error(`Expected 31 repository records, found ${repositories.length}`);

const duplicateRepos = repositories.filter((repo, index) => repositories.findIndex((item) => item.name === repo.name) !== index);
if (duplicateRepos.length) throw new Error(`Duplicate repository entries: ${duplicateRepos.map((repo) => repo.name).join(", ")}`);

console.log(`Validated ${featured.length} case studies, ${repositories.length} repositories, and ${requiredFiles.length} required files.`);
