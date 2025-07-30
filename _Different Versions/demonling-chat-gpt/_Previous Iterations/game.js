class Combatant {
  constructor(name, hp, strength, defense, agility) {
    this.name = name;
    this.maxHp = hp;
    this.hp = hp;
    this.strength = strength;
    this.defense = defense;
    this.agility = agility;
    this.defending = false;
  }

  isAlive() {
    return this.hp > 0;
  }

  attack(target) {
    let baseDamage = this.strength - Math.floor(target.defense / 2);
    let damage = Math.max(1, baseDamage);
    if (target.defending) {
      damage = Math.floor(damage / 2);
    }
    target.hp -= damage;
    return damage;
  }

  defend() {
    this.defending = true;
  }

  endTurn() {
    this.defending = false;
  }
}

const player = new Combatant("Demonling", 20, 5, 2, 3);
const enemy = new Combatant("Goblin Grunt", 15, 4, 1, 2);

function updateStatus() {
  document.getElementById("player-stats").textContent =
    `${player.name}: ${player.hp}/${player.maxHp} HP`;
  document.getElementById("enemy-stats").textContent =
    `${enemy.name}: ${enemy.hp}/${enemy.maxHp} HP`;
}

function log(message) {
  const logDiv = document.getElementById("battle-log");
  logDiv.innerHTML += `<p>${message}</p>`;
  logDiv.scrollTop = logDiv.scrollHeight;
}

function checkVictory() {
  if (!enemy.isAlive()) {
    log("You defeated the Goblin Grunt! Victory!");
    document.getElementById("actions").style.display = "none";
    return true;
  } else if (!player.isAlive()) {
    log("You have been defeated... Game Over.");
    document.getElementById("actions").style.display = "none";
    return true;
  }
  return false;
}

function playerAttack() {
  const dmg = player.attack(enemy);
  log(`You attack the Goblin Grunt for ${dmg} damage.`);
  endTurn();
}

function playerDefend() {
  player.defend();
  log("You brace for the next attack.");
  endTurn();
}

function endTurn() {
  if (checkVictory()) return;

  setTimeout(() => {
    const dmg = enemy.attack(player);
    log(`Goblin Grunt attacks you for ${dmg} damage.`);
    player.endTurn();
    updateStatus();
    checkVictory();
  }, 1000);
}

window.onload = () => {
  updateStatus();
  log("A Goblin Grunt appears! Prepare for battle.");
};