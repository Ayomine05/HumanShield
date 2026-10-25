let currentScenario = null;
let currentStepIndex = 0;
let currentStepId = "start";
let userAnswers = [];

function loadAllData() {
  fetch("/api/summary")
    .then(response => response.json())
    .then(data => {
      document.getElementById("readiness-score").textContent = data.readinessScore ?? "\u2014";
      document.getElementById("weak-skill").textContent = data.weakSkill;
      document.getElementById("tests-completed").textContent = data.testsCompleted;
    });

  fetch("/api/categories")
    .then(response => response.json())
    .then(data => {
      renderCaseList("categories-list", data);

      const priority = [...data]
        .sort((a, b) => (a.lastScore ?? -1) - (b.lastScore ?? -1))
        .slice(0, 4);

      renderCaseList("dashboard-list", priority);
    });

  fetch("/api/history")
    .then(response => response.json())
    .then(data => {
      const body = document.getElementById("history-table-body");

      if (data.length === 0) {
        body.innerHTML = `<tr><td colspan="5">No tests completed yet.</td></tr>`;
        return;
      }

      body.innerHTML = data.map(entry => `
        <tr>
          <td>${entry.date}</td>
          <td>${entry.category}</td>
          <td>${entry.mode}</td>
          <td>${entry.difficulty}</td>
          <td>${entry.score}%</td>
        </tr>
      `).join("");
    });

  fetch("/api/profile")
    .then(response => response.json())
    .then(data => renderProfileBars(data));
}

loadAllData();

function renderProfileBars(skills) {
  const container = document.getElementById("profile-bars");

  container.innerHTML = skills.map(skill => {
    const hasScore = skill.score !== null;
    const width = hasScore ? skill.score : 0;
    const label = hasScore ? `${skill.score}%` : "Not tested";

    return `
      <div class="profile-bar-row">
        <span class="profile-bar-label">${skill.name}</span>
        <span class="profile-bar-track"><span class="profile-bar-fill" style="width: ${width}%"></span></span>
        <span class="profile-bar-value">${label}</span>
      </div>
    `;
  }).join("");
}

function renderCaseList(containerId, categories) {
  const container = document.getElementById(containerId);

  container.innerHTML = categories.map(cat => `
    <div class="case-row">
      <div class="case-row-text">
        <span class="case-row-title">${cat.name}</span>
        <span class="case-row-sub">${cat.sub}</span>
      </div>
      <span class="case-row-tag">${cat.difficulty}</span>
      <span class="case-row-score">${cat.lastScore !== null ? cat.lastScore + "%" : "Not tested"}</span>
      <button class="case-row-action" data-scenario-id="${cat.scenarioId || ""}">${cat.lastScore !== null ? "Retest" : "Start test"}</button>
    </div>
  `).join("");

  container.querySelectorAll(".case-row-action").forEach(button => {
    button.addEventListener("click", () => {
      const scenarioId = button.dataset.scenarioId;
      if (scenarioId) {
        startTest(scenarioId);
      } else {
        alert("No test built yet for this category.");
      }
    });
  });
}

function startTest(scenarioId) {
  fetch(`/api/scenario/${scenarioId}`)
    .then(response => response.json())
    .then(data => {
      currentScenario = data;
      currentStepIndex = 0;
      currentStepId = "start";
      userAnswers = [];

      navLinks.forEach(l => l.classList.remove("is-active"));
      panels.forEach(panel => {
        panel.hidden = panel.dataset.viewPanel !== "test";
      });

      document.getElementById("test-title").textContent = currentScenario.title;
      showStep();
    });
}

function getCurrentStep() {
  if (Array.isArray(currentScenario.steps)) {
    return currentScenario.steps[currentStepIndex];
  }
  return currentScenario.steps[currentStepId];
}

function showStep() {
  const step = getCurrentStep();
  const branching = !Array.isArray(currentScenario.steps);

  if (branching) {
    const badge = currentScenario.adaptive ? "\u26a1 Adaptive call in progress" : "Call in progress";
    document.getElementById("test-progress").textContent = badge;
  } else {
    document.getElementById("test-progress").textContent =
      `Step ${currentStepIndex + 1} of ${currentScenario.steps.length}`;
  }

  document.getElementById("test-message").textContent = step.message;

  const callBar = document.getElementById("test-call-bar");
  if (currentScenario.mode === "voice") {
    callBar.hidden = false;
    document.getElementById("test-listen-btn").onclick = () => {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(step.message);
      window.speechSynthesis.speak(utterance);
    };
  } else {
    callBar.hidden = true;
    window.speechSynthesis.cancel();
  }

  const choicesContainer = document.getElementById("test-choices");
  choicesContainer.innerHTML = step.choices.map(choice => `
    <button class="test-choice-btn" data-choice-id="${choice.id}">${choice.text}</button>
  `).join("");

  document.getElementById("test-feedback").hidden = true;

  choicesContainer.querySelectorAll(".test-choice-btn").forEach(button => {
    button.addEventListener("click", () => {
      const choiceId = button.dataset.choiceId;
      const choice = step.choices.find(c => c.id === choiceId);
      handleChoice(choice);
    });
  });
}

function handleChoice(choice) {
  userAnswers.push({ safe: choice.safe, skill: choice.skill });

  document.getElementById("test-choices").innerHTML = "";

  const feedbackBox = document.getElementById("test-feedback");
  feedbackBox.hidden = false;
  feedbackBox.className = "test-feedback " + (choice.safe ? "is-safe" : "is-risky");

  const branching = !Array.isArray(currentScenario.steps);
  const isLastStep = branching
    ? !choice.next
    : currentStepIndex === currentScenario.steps.length - 1;

  feedbackBox.innerHTML = `
    <p>${choice.feedback}</p>
    <button class="test-feedback-next" id="test-next-btn">${isLastStep ? "See results" : "Next"}</button>
  `;

  document.getElementById("test-next-btn").addEventListener("click", () => {
    if (isLastStep) {
      finishTest();
    } else {
      if (branching) {
        currentStepId = choice.next;
      } else {
        currentStepIndex++;
      }
      showStep();
    }
  });
}

function finishTest() {
  fetch(`/api/scenario/${currentScenario.id}/score`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(userAnswers)
  })
    .then(response => response.json())
    .then(result => {
      return fetch("/api/recommendation")
        .then(response => response.json())
        .then(recommendation => {
          document.getElementById("test-title").textContent = "Test complete";
          document.getElementById("test-progress").textContent = "";
          document.getElementById("test-message").innerHTML = `
            <p>You scored ${result.score}% (${result.safeCount} of ${result.total} safe choices).</p>
            <p><strong>Focus area: ${recommendation.skillName}.</strong> ${recommendation.action}</p>
          `;
          document.getElementById("test-choices").innerHTML = "";
          document.getElementById("test-feedback").hidden = true;

          loadAllData();
        });
    });
}

const navLinks = document.querySelectorAll(".rail-link");
const panels = document.querySelectorAll("[data-view-panel]");

navLinks.forEach(link => {
  link.addEventListener("click", () => {
    window.speechSynthesis.cancel();

    navLinks.forEach(l => l.classList.remove("is-active"));
    link.classList.add("is-active");

    const target = link.dataset.view;

    panels.forEach(panel => {
      panel.hidden = panel.dataset.viewPanel !== target;
    });
  });
});
