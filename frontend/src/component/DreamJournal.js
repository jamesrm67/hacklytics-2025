import React, { useState, useEffect } from "react";
import { onAuthStateChanged } from "firebase/auth";
import { ref, onValue, getDatabase, push } from "firebase/database";
import { auth, app } from "../firebase"; // Import Firebase app instance

function DreamJournal() {
  const [dreams, setDreams] = useState();
  const [selectedDream, setSelectedDream] = useState(null);

  const db = getDatabase(app);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
        if (user) {
          const userId = user.uid;
          console.log('User ID:', userId); 
          const dreamsRef = ref(db, `dreams/${userId}`);
            onValue(dreamsRef, (snapshot) => {
                const dreamsData = snapshot.val();
                const dreamList = [];
                if (dreamsData) {
                    for (const dreamId in dreamsData) {
                        if (dreamsData.hasOwnProperty(dreamId)) {
                            const dream = dreamsData[dreamId]
                            dreamList.push({
                                id: dreamId,
                                dreamText: dream["dream-text"],
                                interpretation: dream.interpretation,
                                sentiment: dream.sentiment,
                                entities: dream.entities,
                            });
                        }
                    }
                }
                setDreams(dreamList);
            }, [dreams]);
        } else {
          // No user is signed in.
          console.log('No user is signed in.');
          setDreams();
          setSelectedDream(null);
          // You might want to redirect to login or handle this case accordingly.
        }
    });
    return () => unsubscribe();
  },);

  const handleDreamSelect = (event) => {
    const selectedId = event.target.value;
    if (selectedId) {
      const selected = dreams.find((dream) => dream.id === selectedId);
      setSelectedDream(selected);
    } else {
      setSelectedDream(null); // Clear selection if no dream is selected
    }
  };

  const writeDreamData = (dreamData) => {
    if (auth.currentUser) {
      const userId = auth.currentUser.uid;
      const dreamsRef = ref(db, `dreams/${userId}`);

      const dreamWithUserId = {...dreamData, user_id: userId };
      push(dreamsRef, dreamWithUserId)
      .then(() => {
          console.log("Dream written successfully!");
        })
      .catch((error) => {
          console.error("Error writing dream:", error);
        });
    } else {
      console.log("User is not logged in")
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const newDream = {
      dreamText: event.target["dream-text"].value, // Use "dream-text"
      interpretation: event.target.interpretation.value,
      sentiment: {
        tone: (event.target.value[0]),
        subjectivity: parseFloat(event.target.value[1]),
      },
      entities: event.target.entities.value.split(",").map(entity => entity.trim()),
    };
    writeDreamData(newDream);
    event.target.reset();
  };

  return (
    <div>
      <h2>My Dreams</h2>
      <select value={selectedDream? selectedDream.id: ""} onChange={handleDreamSelect}>
        <option value="">Select a dream</option>
        {dreams.map((dream) => (
          <option key={dream.id} value={dream.id}>
            {dream.interpretation}
          </option>
        ))}
      </select>

      {selectedDream && (
        <div>
          <h3>{selectedDream.interpretation}</h3>
          <p>User ID: {selectedDream.user_id}</p>
          <p>Dream Text: {selectedDream["dream-text"]}</p> {/* Display dream-text */}
          <p>Sentiment: Polarity: {selectedDream.sentiment.polarity}, Subjectivity: {selectedDream.sentiment.subjectivity}</p>
          <ul>
            {selectedDream.entities.map((entity, index) => (
              <li key={index}>{entity}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Example form (adapt as needed) */}
      <form onSubmit={handleSubmit}>
        <label htmlFor="dream-text">Dream Text:</label> {/* Label for dream-text */}
        <textarea id="dream-text" name="dream-text" /><br /> {/* Input for dream-text */}

        <label htmlFor="interpretation">Interpretation:</label>
        <textarea id="interpretation" name="interpretation" /><br />

        <label htmlFor="polarity">Polarity:</label>
        <input type="number" id="polarity" name="polarity" step="0.1" /><br />

        <label htmlFor="subjectivity">Subjectivity:</label>
        <input type="number" id="subjectivity" name="subjectivity" step="0.1" /><br />

        <label htmlFor="entities">Entities (comma-separated):</label>
        <input type="text" id="entities" name="entities" /><br />

        <button type="submit">Add Dream</button>
      </form>
    </div>
  );
}

export default DreamJournal;