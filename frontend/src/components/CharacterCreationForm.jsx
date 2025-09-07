import React, { useState, useEffect } from "react";
import Dice from "react-dice-roll";
import "./CharacterCreationForm.css";

const CLASSES = [
  "Barbarian", "Bard", "Cleric", "Druid", "Fighter",
  "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer",
  "Warlock", "Wizard"
];
const RACES = ["Human", "Elf", "Dwarf", "Halfling", "Dragonborn", "Gnome", "Half-Orc", "Tiefling"];
const ALIGNMENTS = [
  "Lawful Good", "Neutral Good", "Chaotic Good",
  "Lawful Neutral", "True Neutral", "Chaotic Neutral",
  "Lawful Evil", "Neutral Evil", "Chaotic Evil"
];
const SKILLS = [
  "Acrobatics", "Animal Handling", "Arcana", "Athletics", "Deception",
  "History", "Insight", "Intimidation", "Investigation", "Medicine",
  "Nature", "Perception", "Performance", "Persuasion", "Religion",
  "Sleight of Hand", "Stealth", "Survival"
];
const SAVING_THROWS = ["STR", "DEX", "CON", "INT", "WIS", "CHA"];

const HIT_DICE_BY_CLASS = {
  Barbarian: "1d12",
  Bard: "1d8",
  Cleric: "1d8",
  Druid: "1d8",
  Fighter: "1d10",
  Monk: "1d8",
  Paladin: "1d10",
  Ranger: "1d10",
  Rogue: "1d8",
  Sorcerer: "1d6",
  Warlock: "1d8",
  Wizard: "1d6"
};

function TabNav({ tabs, activeTab, setActiveTab }) {
  return (
    <nav className="tab-nav">
      {tabs.map((tab, i) => (
        <button
          key={tab}
          onClick={() => setActiveTab(i)}
          className={activeTab === i ? "active" : ""}
          type="button"
        >
          {tab}
        </button>
      ))}
    </nav>
  );
}

function BasicsTab({ form, setForm }) {
  return (
    <>
      <label>Name</label>
      <input
        style={{ width: "100%", maxWidth: "400px", fontFamily: "'Georgia', serif" }}
        value={form.name}
        type="text"
        onChange={e => setForm({ ...form, name: e.target.value })}
      />
      <label>Class</label>
      <select
        value={form.class}
        onChange={e => setForm({ ...form, class: e.target.value })}
      >
        <option value="">Select Class</option>
        {CLASSES.map(c => <option key={c}>{c}</option>)}
      </select>
      <label>Race</label>
      <select
        value={form.race}
        onChange={e => setForm({ ...form, race: e.target.value })}
      >
        <option value="">Select Race</option>
        {RACES.map(r => <option key={r}>{r}</option>)}
      </select>
      <label>Level</label>
      <input
        type="number"
        min={1}
        max={20}
        value={form.level}
        onChange={e => {
          let lvl = +e.target.value;
          if (lvl < 1) lvl = 1;
          if (lvl > 20) lvl = 20;
          setForm({ ...form, level: lvl });
        }}
      />
      <label>Proficiency Bonus</label>
      <input
        type="number"
        value={form.proficiencyBonus}
        onChange={e => setForm({ ...form, proficiencyBonus: +e.target.value })}
      />
    </>
  );
}

function AbilitiesTab({ form, setForm }) {
  // 6 stats, each needs 4 dice rolls (4d6 drop lowest)
  const [rolling, setRolling] = useState(false);
  const [diceRolls, setDiceRolls] = useState(Array(6).fill(null).map(() => Array(4).fill(null)));

  const startRolling = () => {
    setRolling(true);
    setDiceRolls(Array(6).fill(null).map(() => Array(4).fill(null)));
  };

  const onDieRollComplete = (statIndex, dieIndex, value) => {
    setDiceRolls(prev => {
      const copy = prev.map(arr => arr.slice());
      copy[statIndex][dieIndex] = value;

      if (copy.every(arr => arr.every(v => v !== null))) {
        const rolledStats = copy.map(arr => {
          const sorted = arr.slice().sort((a,b) => b - a);
          return sorted[0] + sorted[1] + sorted[2];
        });
        const statsKeys = Object.keys(form.abilityScores);
        const newAbilities = {};
        statsKeys.forEach((stat, i) => newAbilities[stat] = rolledStats[i]);
        setForm(prev => ({ ...prev, abilityScores: newAbilities }));
        setRolling(false);
      }

      return copy;
    });
  };

  const abilityScores = form.abilityScores;
  const statsKeys = Object.keys(abilityScores);

  const handleAssign = (stat, value) => {
    setForm(prev => ({
      ...prev,
      abilityScores: {
        ...prev.abilityScores,
        [stat]: Number(value)
      }
    }));
  };

  return (
    <div style={{ position: "relative" }}>
      <button onClick={startRolling} disabled={rolling} style={{ marginBottom: "1rem" }}>
        Roll Stats (4d6 drop lowest)
      </button>

      <div style={{ marginBottom: "1rem" }}>
        <strong>Current Ability Scores:</strong>{" "}
        {statsKeys.map(stat => (
          <span key={stat} style={{ marginRight: 10 }}>
            {stat}: {abilityScores[stat]}
          </span>
        ))}
      </div>

      {!rolling && (
        <>
          {statsKeys.map(stat => (
            <div key={stat} className="ability-row">
              <label>{stat}</label>
              <input
                type="number"
                value={abilityScores[stat]}
                min={3}
                max={20}
                onChange={e => handleAssign(stat, e.target.value)}
              />
            </div>
          ))}

          <label>Armor Class (AC)</label>
          <input
            type="number"
            value={form.ac}
            onChange={e => setForm({ ...form, ac: +e.target.value })}
          />
          <label>Initiative</label>
          <input
            type="number"
            value={form.initiative}
            onChange={e => setForm({ ...form, initiative: +e.target.value })}
          />
          <label>Speed</label>
          <input
            type="number"
            value={form.speed}
            onChange={e => setForm({ ...form, speed: +e.target.value })}
          />
          <label>Hit Dice</label>
          <input
            type="text"
            value={form.hitDice}
            readOnly
          />
          <label>Current HP</label>
          <input
            type="number"
            value={form.currentHp}
            onChange={e => setForm({ ...form, currentHp: +e.target.value })}
          />
          <label>Max HP</label>
          <input
            type="number"
            value={form.maxHp}
            onChange={e => setForm({ ...form, maxHp: +e.target.value })}
          />
        </>
      )}

      {rolling && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: "rgba(0,0,0,0.85)",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            zIndex: 1000,
            padding: 40,
            boxSizing: "border-box",
            borderRadius: 8,
            overflowY: "auto",
          }}
        >
          <h2 style={{ color: "white", marginBottom: "2rem" }}>
            Rolling Stats...
          </h2>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(4, 70px)",
              gridGap: 20,
              backgroundColor: "rgba(255,255,255,0.1)",
              padding: 30,
              borderRadius: 10,
            }}
          >
            {diceRolls.map((diceGroup, statIndex) =>
              diceGroup.map((_, dieIndex) => (
                <Dice
                  key={`${statIndex}-${dieIndex}`}
                  size={60}
                  onRollComplete={val => onDieRollComplete(statIndex, dieIndex, val)}
                />
              ))
            )}
          </div>
          <small style={{ color: "white", marginTop: 25, fontSize: 14 }}>
            Each group of 4 dice = one stat (sum highest 3)
          </small>
        </div>
      )}
    </div>
  );
}

function SkillsTab({ form, setForm }) {
  const toggleSkill = (skill, level) => {
    setForm(prev => {
      const current = prev.skills[skill] || { proficient: false, expert: false };
      let updated;
      if (level === "proficient") {
        updated = {
          ...current,
          proficient: !current.proficient,
          expert: current.expert && !current.proficient ? false : current.expert
        };
      } else {
        updated = {
          ...current,
          expert: !current.expert,
          proficient: !current.expert ? true : current.proficient
        };
      }
      return { ...prev, skills: { ...prev.skills, [skill]: updated } };
    });
  };

  const toggleSavingThrow = (stat) => {
    setForm(prev => ({
      ...prev,
      savingThrows: {
        ...prev.savingThrows,
        [stat]: !prev.savingThrows[stat]
      }
    }));
  };

  return (
    <>
      <h4>Skills</h4>
      {SKILLS.map(skill => {
        const val = form.skills[skill] || { proficient: false, expert: false };
        return (
          <div key={skill} className="skill-row">
            <label>{skill}</label>
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={val.proficient}
                onChange={() => toggleSkill(skill, "proficient")}
              />
              Proficient
            </label>
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={val.expert}
                onChange={() => toggleSkill(skill, "expert")}
              />
              Expert
            </label>
          </div>
        );
      })}
      <h4>Saving Throws</h4>
      {SAVING_THROWS.map(stat => (
        <label
          key={stat}
          className="checkbox-label"
          style={{ display: "block", marginTop: "0.3rem" }}
        >
          <input
            type="checkbox"
            checked={form.savingThrows[stat] || false}
            onChange={() => toggleSavingThrow(stat)}
          />
          {stat}
        </label>
      ))}
    </>
  );
}

function SpellcastingTab({ form, setForm }) {
  return (
    <>
      <label>Spell Slots</label>
      <input
        type="number"
        min={0}
        max={9}
        value={form.spellSlots}
        onChange={e => setForm({ ...form, spellSlots: +e.target.value })}
      />
      <label>Cantrips Known</label>
      <input
        type="number"
        min={0}
        value={form.cantrips}
        onChange={e => setForm({ ...form, cantrips: +e.target.value })}
      />
    </>
  );
}

function AppearanceTab({ form, setForm }) {
  return (
    <>
      <label>Class Features</label>
      <textarea readOnly value={form.classFeatures} rows={3} />
      <label>Racial Traits</label>
      <textarea readOnly value={form.racialTraits} rows={3} />
      <label>Equipment</label>
      <textarea readOnly value={form.equipment} rows={3} />
      <label>Background (Advanced)</label>
      <textarea
        value={form.advancedBackground}
        onChange={e => setForm({ ...form, advancedBackground: e.target.value })}
        rows={3}
      />
      <label>Notes</label>
      <textarea
        value={form.notes}
        onChange={e => setForm({ ...form, notes: e.target.value })}
        rows={3}
      />
      <label>Alignment</label>
      <select
        value={form.alignment}
        onChange={e => setForm({ ...form, alignment: e.target.value })}
      >
        <option value="">Select Alignment</option>
        {ALIGNMENTS.map(a => <option key={a}>{a}</option>)}
      </select>
    </>
  );
}

export default function CharacterCreationForm() {
  const tabs = ["Basics", "Abilities", "Skills", "Spellcasting", "Appearance & Personality"];
  const [activeTab, setActiveTab] = useState(0);

  const [form, setForm] = useState({
    name: "",
    class: "",
    race: "",
    level: 1,
    proficiencyBonus: 2,
    abilityScores: { STR: 8, DEX: 8, CON: 8, INT: 8, WIS: 8, CHA: 8 },
    ac: 10,
    initiative: 0,
    speed: 30,
    hitDice: "",
    currentHp: 10,
    maxHp: 10,
    skills: {},
    savingThrows: {},
    spellSlots: 0,
    cantrips: 0,
    classFeatures: "Class features here...",
    racialTraits: "Racial traits here...",
    equipment: "Equipment here...",
    advancedBackground: "",
    notes: "",
    alignment: ""
  });

  useEffect(() => {
    if (form.class && HIT_DICE_BY_CLASS[form.class]) {
      setForm(prev => ({ ...prev, hitDice: HIT_DICE_BY_CLASS[form.class] }));
    } else {
      setForm(prev => ({ ...prev, hitDice: "" }));
    }
  }, [form.class]);

  return (
    <div className="character-creation">
      <h1>Character Creation</h1>
      <TabNav tabs={tabs} activeTab={activeTab} setActiveTab={setActiveTab} />
      <div style={{ minHeight: 400 }}>
        {activeTab === 0 && <BasicsTab form={form} setForm={setForm} />}
        {activeTab === 1 && <AbilitiesTab form={form} setForm={setForm} />}
        {activeTab === 2 && <SkillsTab form={form} setForm={setForm} />}
        {activeTab === 3 && <SpellcastingTab form={form} setForm={setForm} />}
        {activeTab === 4 && <AppearanceTab form={form} setForm={setForm} />}
      </div>
    </div>
  );
}
