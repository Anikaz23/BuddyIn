import json
import re
from openai_model import OpenAIModel

openai_model = OpenAIModel()

with open('testing_cases/hard_high', 'r') as f:
    content = f.read()

job_descriptions = []
sections = re.split(r'^## \d+$', content, flags=re.MULTILINE)

for section in sections:
    desc = section.strip()
    if desc:
        job_descriptions.append(desc)

with open('testing_cases/hard_high_output.txt', 'w') as f:
    for inx, desc in enumerate(job_descriptions):
        res = json.loads(openai_model.parse_description(desc))
        f.write("##" + str(inx) )
        for key in res:
            f.write("\n" + key + ":")
            for item in res[key]:
                if( key == "experience" or key == "degree"):
                    f.write("" + item)
                else:
                    f.write("\n- " + item)
        f.write("\n\n")

print("Testing completed. Results written to 'testing_cases/hard_high_output'.")