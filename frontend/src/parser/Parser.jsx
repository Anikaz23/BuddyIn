import { useRef, useContext } from 'react'
import axios from 'axios'
import { Navigate } from 'react-router-dom'

export default function Parser() {

    const { setKeyWords } = useContext(KeyWordsContext);


    const getJobDescription = async () => {
        const textAreaValue = textAreaRef.current.value;
        try{
            const response =  await axios.post('http://localhost:5000/parse', {jobDescription: textAreaValue});
            if(response.status === 201){
                const kResponse = await axios.get('http://localhost:5000/analyze');
                if(kResponse.status === 200) {
                    setKeyWords(kResponse.data);
                    <Navigate to="/editor" />

                }
                else console.error("Failed to get analyzed job description. Status code:", kResponse.status);
            }
            else console.error("Failed to parse job description. Status code:", response.status);
        }
        catch (error){
            console.error("Error during parsing:", error);
        }
    }
    const textAreaRef = useRef(null);

    return (
    <div>
      <textarea ref={textAreaRef}></textarea>
      <button onClick={getJobDescription}>Parse</button>
    </div>
    )
}

