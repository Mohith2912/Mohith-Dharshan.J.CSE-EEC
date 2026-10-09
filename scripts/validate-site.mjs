import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import { createHash } from "node:crypto";
import vm from "node:vm";

const root = resolve(import.meta.dirname, "..");
const requiredFiles = [
  "index.html",
  "styles.css",
  "js/app.js",
  "js/projects.js",
  "assets/mohith-dharshan.jpg",
  "assets/Mohith_Dharshan_Resume.pdf",
  "assets/Mohith_Dharshan_Resume_Original.pdf",
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

if (!html.includes('href="tel:+917845122655"')) {
  throw new Error("Missing clickable contact phone number");
}

if (!html.includes('class="theme-toggle"') || !html.includes('mohith-portfolio-theme')) {
  throw new Error("Responsive light/dark theme controls are missing");
}

for (const resume of ["Mohith_Dharshan_Resume_Original.pdf", "Mohith_Dharshan_Resume.pdf"]) {
  const resumeHref = `assets/${resume}`;
  if (!html.includes(`href="${resumeHref}" target="_blank"`)) {
    throw new Error(`Missing view action for ${resume}`);
  }
  if (!html.includes(`href="${resumeHref}" download=`)) {
    throw new Error(`Missing download action for ${resume}`);
  }
}

const originalResumeHash = createHash("sha256")
  .update(readFileSync(resolve(root, "assets/Mohith_Dharshan_Resume_Original.pdf")))
  .digest("hex");
if (originalResumeHash !== "c0bb40e7dc392bcf0a99311f9e36ca733c48040f4af5f4f218266facd85e6288") {
  throw new Error("The original attached résumé PDF was modified");
}

const context = { window: {} };
vm.createContext(context);
vm.runInContext(readFileSync(resolve(root, "js/projects.js"), "utf8"), context);
const { featured, repositories } = context.window.PORTFOLIO_DATA;

if (featured.length !== 7) throw new Error(`Expected 7 featured projects, found ${featured.length}`);
if (repositories.length !== 30) throw new Error(`Expected 30 project repository records, found ${repositories.length}`);

if (repositories.some((repo) => repo.name === "Mohith2912")) {
  throw new Error("GitHub profile README must remain separate from the project repository atlas");
}

const expectedLiveProjects = new Map([
  ["college-ext", "https://beyond-syllabus-learn.vercel.app"],
  ["voe", "https://voe-web-gilt.vercel.app"],
  ["urban-furniture", "https://urban-furniture-web.vercel.app"],
  ["peoplepay360", "https://people-pay360-mu.vercel.app"]
]);

for (const [id, expectedUrl] of expectedLiveProjects) {
  const project = featured.find((item) => item.id === id);
  if (!project) throw new Error(`Missing featured project: ${id}`);
  if (project.live !== expectedUrl) throw new Error(`Unexpected live URL for ${id}: ${project.live}`);
}

const appSource = readFileSync(resolve(root, "js/app.js"), "utf8");
if (!appSource.includes('systemTheme.addEventListener("change"') || !appSource.includes("applyTheme(nextTheme, true)")) {
  throw new Error("Theme switching must follow the system and persist a manual choice");
}
if (!appSource.includes('data-live-project="${project.id}"')) {
  throw new Error("Live project links are missing their navigation marker");
}
const newTabLiveLinks = appSource.match(/href="\$\{project\.live\}"[^>]*target="_blank"[^>]*rel="noopener noreferrer"/g) ?? [];
if (newTabLiveLinks.length !== 2) {
  throw new Error("Both featured-card and case-study live links must open safely in a new tab");
}

const duplicateRepos = repositories.filter((repo, index) => repositories.findIndex((item) => item.name === repo.name) !== index);
if (duplicateRepos.length) throw new Error(`Duplicate repository entries: ${duplicateRepos.map((repo) => repo.name).join(", ")}`);

console.log(`Validated ${featured.length} case studies, ${repositories.length} repositories, and ${requiredFiles.length} required files.`);
