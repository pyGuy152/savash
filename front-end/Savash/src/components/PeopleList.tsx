import { useState, useEffect } from "react";
import { getPeopleFromClass, Person } from "../types.ts";

interface PeopleListProp {
    classID : number;
}

function PeopleList({classID}: PeopleListProp) {

    const [people, setPeople] = useState<Person[]>([]);

    async function updatePeople(){
        let data = await getPeopleFromClass(classID);
        if(data){ 
            setPeople(data);
        }
        console.log(data);
    }

    useEffect(() => {
        updatePeople();
    }, [])

    if(people.length === 0 || !Array.isArray(people)){
        return <h1>Empty class?</h1>;
    }
    else{
        return (
          <>
            <ul className="people-list">
              {people.map((e, i) => (
                <li key={i} className="person-row">
                  <p className="left">
                    {e.name}
                    <span className="username">({e.username})</span>
                  </p>
                  <div className="middle">
                    <p>{e.email}</p>
                    <button className="kick">Kick</button>
                  </div>
                </li>
              ))}
            </ul>
          </>
        );
    }
}
export default PeopleList;

