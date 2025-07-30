const quests = [
  {
    title: "A Soul in the Dirt",
    desc: "You wake in ash and bone. Defeat a lurking monster to prove your will.",
    reward: "Unlocks: Goblin Grunt minion. +10 XP, +25 Gold, +1 Soul Shard",
    completed: false
  },
  {
    title: "Scraps of a Forgotten Fortress",
    desc: "Scavenge old ruins for the foundation of your future dungeon.",
    reward: "Unlocks: Throne Room blueprint. +10 XP, +20 Gold, +1 Soul Shard",
    completed: false
  },
  {
    title: "Fire in the Veins",
    desc: "Absorb corrupted soul energy from a broken idol.",
    reward: "Unlocks: Soul Ritual Room. +15 XP, +30 Gold, +1 Soul Shard",
    completed: false
  }
];

const questChainDiv = document.getElementById("quest-chain");
const questDetails = document.getElementById("quest-details");
const questResult = document.getElementById("quest-result");
const questTitle = document.getElementById("quest-title");
const questDesc = document.getElementById("quest-desc");
const questReward = document.getElementById("quest-reward");
const startQuestBtn = document.getElementById("start-quest");

let selectedQuestIndex = null;

function loadQuests() {
  questChainDiv.innerHTML = "";
  quests.forEach((quest, index) => {
    const btn = document.createElement("button");
    btn.textContent = quest.completed ? `${quest.title} ✔` : quest.title;
    btn.disabled = quest.completed || (index > 0 && !quests[index - 1].completed);
    btn.onclick = () => showQuestDetails(index);
    questChainDiv.appendChild(btn);
  });
}

function showQuestDetails(index) {
  selectedQuestIndex = index;
  const quest = quests[index];
  questTitle.textContent = quest.title;
  questDesc.textContent = quest.desc;
  questDetails.style.display = "block";
  questResult.style.display = "none";
}

startQuestBtn.onclick = () => {
  if (selectedQuestIndex !== null) {
    quests[selectedQuestIndex].completed = true;
    questDetails.style.display = "none";
    questReward.textContent = quests[selectedQuestIndex].reward;
    questResult.style.display = "block";
    loadQuests();
  }
};

function returnToQuests() {
  questResult.style.display = "none";
  selectedQuestIndex = null;
}

window.onload = loadQuests;
