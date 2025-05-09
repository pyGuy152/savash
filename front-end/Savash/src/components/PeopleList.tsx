
interface PeopleListProp {
    classID : number;
}

function PeopleList({classID}: PeopleListProp) {
    return (<h1>{classID}</h1>)
}

export default PeopleList;
