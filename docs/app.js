const mappings = {
  "branch-protection-disabled": {
    title: "Default branch protection is disabled",
    refs: [
      ["ISO/IEC 27001:2022", "A.8.32", "Change management", "SUPPORTING"],
      ["NIS2", "Article 21(2)(e)", "Secure acquisition, development and maintenance", "CONTEXTUAL"],
      ["SOC 2", "CC8.1", "Change management", "SUPPORTING"],
      ["ENS", "mp.sw.1 / mp.sw.2", "Software development and acceptance", "CONTEXTUAL"]
    ],
    evidence: ["Branch protection configuration", "Change approval workflow", "Repository governance policy"]
  },
  "required-pr-reviews-disabled": {
    title: "Required pull-request reviews are disabled",
    refs: [
      ["ISO/IEC 27001:2022", "A.8.32", "Change management", "SUPPORTING"],
      ["SOC 2", "CC8.1", "Change management", "SUPPORTING"],
      ["ENS", "op.acc.3", "Segregation of duties", "CONTEXTUAL"]
    ],
    evidence: ["Pull-request approval rules", "Reviewer assignment evidence", "Change records"]
  },
  "secret-scanning-disabled": {
    title: "Secret scanning is disabled",
    refs: [
      ["ISO/IEC 27001:2022", "A.5.17", "Authentication information", "SUPPORTING"],
      ["ISO/IEC 27001:2022", "A.8.24", "Use of cryptography", "CONTEXTUAL"],
      ["NIS2", "Article 21(2)(j)", "Authentication mechanisms", "CONTEXTUAL"],
      ["ENS", "op.acc.4", "Access-rights management", "CONTEXTUAL"]
    ],
    evidence: ["Secret scanning configuration", "Credential management procedure", "Secret rotation evidence"]
  },
  "dependabot-config-missing": {
    title: "Dependabot configuration is missing",
    refs: [
      ["ISO/IEC 27001:2022", "A.8.8", "Management of technical vulnerabilities", "SUPPORTING"],
      ["NIS2", "Article 21(2)(e)", "Secure maintenance", "CONTEXTUAL"]
    ],
    evidence: ["Dependency management configuration", "Vulnerability remediation records", "Dependency review evidence"]
  }
};

const select = document.querySelector("#finding");
const result = document.querySelector("#result");
for (const [key, value] of Object.entries(mappings)) {
  const option = document.createElement("option");
  option.value = key;
  option.textContent = value.title;
  select.appendChild(option);
}

function render() {
  const item = mappings[select.value];
  result.innerHTML = `<h2>${item.title}</h2><p class="meta">Potential supporting references</p>` +
    item.refs.map(([framework, reference, title, confidence]) => `
      <article class="card">
        <h3>${framework} ${reference}<span class="badge">${confidence}</span></h3>
        <div class="meta">${title}</div>
      </article>`).join("") +
    `<article class="card"><h3>Evidence to review</h3><ul class="evidence">${item.evidence.map(x => `<li>${x}</li>`).join("")}</ul></article>`;
}

document.querySelector("#mapButton").addEventListener("click", render);
render();
