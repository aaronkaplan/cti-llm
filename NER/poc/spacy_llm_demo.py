import logging

from spacy_llm import logger
from spacy_llm.util import assemble

logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.ERROR)

nlp = assemble("config.cfg")

# Example usage
doc = nlp("""
This advisory provides observed tactics, techniques, and procedures (TTPs), indicators of
compromise (IOCs), and recommendations to mitigate the threat posed by APT28 threat actors
related to compromised EdgeRouters. Given the global popularity of EdgeRouters, the FBI and its
international partners urge EdgeRouter network defenders and users to apply immediately the
recommendations in the Mitigations section of this CSA to reduce the likelihood and impact of
cybersecurity incidents associated with APT28 activity.
Ubiquiti EdgeRouters have a user-friendly, Linux-based operating system that makes them popular
for both consumers and malicious cyber actors. EdgeRouters are often shipped with default
credentials and limited to no firewall protections to accommodate wireless internet service providers
(WISPs). Additionally, EdgeRouters do not automatically update firmware unless a consumer
configures them to do so.
          """)

# Print entities
print(doc.to_json())

for ent in doc.ents:
    print(ent.text, ent.label_)