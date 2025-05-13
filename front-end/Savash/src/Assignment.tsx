
import { useEffect, useState } from "react";
import { getAssignment } from "./types.ts"

function Assignment() {

    let [assignmentData, setAssignmentData] = useState(0);

    async function updateAssignmentData(){
        let data = await getAssignment(0);
        setAssignmentData(Number(data));
    }

    useEffect(() => {
        updateAssignmentData();
    }, [])

    return <>
        <h1>Assignments</h1>
        <p>{assignmentData}</p>
    </>
}

export default Assignment;