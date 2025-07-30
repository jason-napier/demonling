
const state = {
  level: 1,
  xp: 0,
  xpToNext: 10,
  mana: 10,
  attack: 5,
  defense: 3,
  agility: 4,
  magic: 2,
  energy: 10,
  energyMax: 10,
  gold: 100,
  soulShards: 0,
  lastEnergyTime: Date.now(),
  completedQuests: []
};

const questChains = {
  "Ash and Bone": [
    { id: "quest1", title: "A Soul in the Dirt", desc: "Defeat a lurking monster.", reward: { xp: 5, gold: 10, soulShard: true } },
    { id: "quest2", title: "Burn the Gate", desc: "Destroy the hero camp entrance.", reward: { xp: 6, gold: 12, soulShard: false } },
    { id: "quest3", title: "Torch the Banner", desc: "Banish their hope.", reward: { xp: 8, gold: 15, soulShard: false } },
    { id: "quest4", title: "The Knight\'s Last Stand", desc: "Boss battle to end the chain.", reward: { xp: 10, gold: 20, soulShard: true } },
    {
      id: "quest1",
      title: "A Soul in the Dirt",
      desc: "Defeat a lurking monster.",
      reward: { xp: 5, gold: 10, soulShard: true }
    },
    {
      id: "quest2",
      title: "Burn the Gate",
      desc: "Destroy the hero camp entrance.",
      reward: { xp: 6, gold: 12, soulShard: false }
    }
  ]
};

let currentQuest = null;

function saveGame() {
  state.lastEnergyTime = Date.now();
  localStorage.setItem("demonlingSave", JSON.stringify(state));
}

function loadGame() {
  const save = localStorage.getItem("demonlingSave");
  if (save) {
    const savedState = JSON.parse(save);
    Object.assign(state, savedState);
    regenerateEnergy();
  }
}

function regenerateEnergy() {
  const now = Date.now();
  const diffMin = Math.floor((now - state.lastEnergyTime) / 60000);
  if (diffMin > 0 && state.energy < state.energyMax) {
    state.energy = Math.min(state.energy + diffMin, state.energyMax);
  }
  updateUI();
}

function gainXP(amount) {
  state.xp += amount;
  if (state.xp >= state.xpToNext) {
    state.level++;
    state.xp -= state.xpToNext;
    state.xpToNext = Math.floor(state.xpToNext * 1.5);
    log("Level up! You are now level " + state.level);
  }
}

function selectQuest(chainTitle, questIndex = 0) {
  const quests = questChains[chainTitle];
  if (!quests) {
    log("No quests found for this chain.");
    return;
  }

  
  let questButtonsHTML = '';
  quests.forEach((quest, index) => {
    const isCompleted = state.completedQuests.includes(quest.id);
    const isUnlocked = index === 0 || state.completedQuests.includes(quests[index - 1].id);

    const status = isCompleted ? '✅ Completed' : isUnlocked ? '🟢 Unlocked' : '🔒 Locked';
    const disabled = isUnlocked ? '' : 'disabled';

    questButtonsHTML += `
      <button ${disabled} onclick="selectQuest('${chainTitle}', ${index})">${quest.title} - ${status}</button><br>
    `;
  });

  document.getElementById("quest-title").innerHTML = "Quests in " + chainTitle;
  document.getElementById("quest-desc").innerHTML = questButtonsHTML;
  document.getElementById("quest-details").style.display = "block";
  
    currentQuest = quests[questIndex];
    document.getElementById("quest-title").textContent = quest.title;
    document.getElementById("quest-desc").textContent = quest.desc;
    document.getElementById("quest-details").style.display = "block";
    return;
  }
}

function startQuest() {
  if (!currentQuest) return;
  if (state.energy < 3) {
    log("Not enough energy to start quest!");
    return;
  }

  state.energy -= 3;
  gainXP(currentQuest.reward.xp);
  state.gold += currentQuest.reward.gold;

  const isFirstClear = !state.completedQuests.includes(currentQuest.id);
  if (currentQuest.reward.soulShard && isFirstClear) {
    state.soulShards += 1;
    log("First time clear! You gained 1 Soul Shard.");
  }

  if (isFirstClear) {
    state.completedQuests.push(currentQuest.id);
  }

  log(`Quest completed! +${currentQuest.reward.xp} XP, +${currentQuest.reward.gold} Gold.`);
  updateUI();
  saveGame();
}

function refillEnergy() {
  state.energy = state.energyMax;
  log("Energy refilled to max (Test Only)");
  updateUI();
  saveGame();
}

function updateUI() {
  document.getElementById("level").textContent = "Level: " + state.level;
  document.getElementById("xp").textContent = "XP: " + state.xp + " / " + state.xpToNext;
  document.getElementById("mana").textContent = "Mana: " + state.mana;
  document.getElementById("attack").textContent = "Attack: " + state.attack;
  document.getElementById("defense").textContent = "Defense: " + state.defense;
  document.getElementById("agility").textContent = "Agility: " + state.agility;
  document.getElementById("magic").textContent = "Magic: " + state.magic;
  document.getElementById("energy-val").textContent = state.energy;
  document.getElementById("gold").textContent = "Gold: " + state.gold;
  document.getElementById("soul-shards").textContent = "Soul Shards: " + state.soulShards;
}

function log(message) {
  const entry = document.createElement("p");
  entry.textContent = message;
  document.getElementById("log-entries").prepend(entry);
}

window.onload = () => {
  loadGame();
  updateUI();
  setInterval(() => {
    regenerateEnergy();
    saveGame();
  }, 60000);
};

document.addEventListener("DOMContentLoaded", () => {
  const ashBoneBtn = document.getElementById("ashBoneBtn");
  if (ashBoneBtn) {
    ashBoneBtn.addEventListener("click", () => selectQuest('Ash and Bone'));
  }
});
