NEW_INSENT_TOKEN = "<t>"
ORD_A = 97

TEMPLATE_ACE_Role = {
    "Business.Declare-Bankruptcy": {
        "Org": 'Failing or bankrupt companies/organizations.',
    },
    "Business.End-Org": {
        "Org": 'Dissolved or dissolving companies/organizations.',
        "Place": 'The location of a dissolved or dissolving companies/organizations.'
    },
    "Business.Merge-Org": {
        "Org": 'Companies or organizations involved in a merger.',
    },
    "Business.Start-Org": {
        "Agent": 'The individuals or entities that founded the company or organization.',
        "Org": 'The company or organization that has been created.',
        "Place": 'The location of the created company or organization.'
    },
    "Conflict.Attack": {
        "Attacker": 'The organization or individuals initiating the attack.',
        "Target": 'The target of the attack.',
        "Instrument": 'The instruments used by the attacker.',
        "Place": 'The location where the attack occurred.',
    },
    "Conflict.Demonstrate": {
        "Entity": 'The entities participating in the parade.',
        "Place": 'The location where the parade occurred.'
    },
    "Contact.Meet": {
        "Entity": 'Multiple entities participating in the meeting.',
        "Place": 'The location where the meeting took place.'
    },
    "Contact.Phone-Write": {
        "Entity": 'Entities participating in remote communication such as phone or email.',
        "Place": 'The location of the entities.'
    },
    "Justice.Acquit": {
        "Defendant": 'The individuals or organizations acquitted for release.',
        "Adjudicator": 'Adjudicator for determining acquittal.'
    },
    "Justice.Appeal": {
        "Plaintiff": 'The plaintiff appealing the decision.',
        "Place": 'The location where the plaintiff is appealing.',
        "Adjudicator": 'The adjudicators ruling on the appeal.'
    },
    "Justice.Arrest-Jail": {
        "Person": 'The individuals or organizations that have been arrested.',
        "Agent": 'The individuals or organizations conducting the arrest.',
        "Place": 'The location where the arrest took place.'
    },
    "Justice.Charge-Indict": {
        "Defendant": 'The individuals or organizations that have been charged',
        "Prosecutor": 'The entity or individual bringing the charges.',
        "Place": 'The place where charges are made.',
        "Adjudicator": 'Adjudicators conducting charge trials.'
    },
    "Justice.Convict": {
        "Defendant": 'The individuals or organizations considered to be criminals.',
        "Place": 'The place where the conviction was made.',
        "Adjudicator": 'Adjudicators determining the conviction.',
    },
    "Justice.Execute": {
        "Person": 'The person who have been executed.',
        "Agent": 'The individuals or organizations carrying out the execution.',
        "Place": 'The place where the execution took place.',
    },
    "Justice.Extradite": {
        "Destination": 'The destination for extradition.',
        "Origin": 'The point of origin for extradition.',
        "Agent": 'The individuals or organizations conducting the extradition.'
    },
    "Justice.Fine": {
        "Entity": 'The individuals or organizations fined.',
        "Place": 'The location where the fine is imposed.',
        "Adjudicator": 'Adjudicators determining the fine.'
    },
    "Justice.Pardon": {
        "Defendant": 'Individuals or organizations who have been pardoned.',
        "Adjudicator": 'The individuals or organizations granting pardons.',
        "Place": 'The entity or jurisdiction granting pardons.'
    },
    "Justice.Release-Parole": {
        "Person": 'Person released or paroled.',
        "Entity": 'Individual or organization requesting release or parole.',
        "Place": 'Location where release or parole takes place.'
    },
    "Justice.Sentence": {
        "Defendant": 'Individual or organization sentenced.',
        "Place": 'Location where sentencing occurs.',
        "Adjudicator": 'Individual or organization adjudicating the sentence.'
    },
    "Justice.Sue": {
        "Defendant": 'Individual or organization being sued.',
        "Plaintiff": 'Individual or organization initiating the suit.',
        "Place": 'Location where the lawsuit is filed.',
        "Adjudicator": 'Adjudicator adjudicating the suit.'
    },
    "Justice.Trial-Hearing": {
        "Defendant": 'Individual or organization being interrogated or tried.',
        "Prosecutor": 'Prosecutor.',
        "Place": 'Location of the interrogation or trial.',
        "Adjudicator": 'Individual or organization conducting the trial or hearing.'
    },
    "Life.Be-Born": {
        "Person": 'Person being born.',
        "Place": 'Place of birth.'
    },
    "Life.Die": {
        "Agent": "Individual or organization causing the victim's death.",
        "Victim": 'Deceased victim.',
        "Instrument": 'Instrument causing death.',
        "Place": 'Location where the death occurred.'
    },
    "Life.Divorce": {
        "Person": 'Individual involved in the divorce.',
        "Place": 'Location where the divorce occurred.'
    },
    "Life.Injure": {
        "Agent": 'Individual or organization causing injury to the victim.',
        "Victim": 'Injured victim.',
        "Instrument": 'Instrument causing injury.',
        "Place": 'Location where the injury occurred.'
    },
    "Life.Marry": {
        "Person": 'Individual getting married.',
        "Place": 'Location of the marriage.'
    },
    "Movement.Transport": {
        "Artifact": "Individual or organization being transported.",
        "Destination": "Final destination of the transport.",
        "Origin": "Starting point of the transport.",
        "Vehicle": "Vehicle used for the transport.",
        "Agent": "Individual or organization facilitating the transport."
    },
    "Personnel.Elect": {
        "Person": "Individual or organization elected.",
        "Entity": "Organization or position appointed through election.",
        "Place": "Location where the election occurs."
    },
    "Personnel.End-Position": {
        "Person": "Individual leaving the position.",
        "Entity": "Company or organization where the departure occurs.",
        "Place": "Location where the departure occurs."
    },
    "Personnel.Nominate": {
        "Person": "Individual or organization involved in the nomination.",
        "Agent": "Individual or organization prompting the nomination."
    },
    "Personnel.Start-Position": {
        "Person": "Individual taking up the position.",
        "Entity": "Company or organization where the position is taken.",
        "Place": "Location where the position is taken."
    },
    "Transaction.Transfer-Money": {
        "Giver": "Individual or organization giving the funds.",
        "Recipient": "Individual or organization receiving the funds.",
        "Place": "Location where the funds are used.",
        "Beneficiary": "Individual or organization benefiting from the funds."
    },
    "Transaction.Transfer-Ownership": {
        "Buyer": "Buyer of the transferred ownership.",
        "Artifact": "Asset being transferred.",
        "Seller": "Seller transferring the ownership.",
        "Place": "Location where the asset transfer occurs.",
        "Beneficiary": "Beneficiary of the asset transfer."
    }
}


TEMPLATE_ACE_Event = {
    "Business.Declare-Bankruptcy": {
        "event subtype": "declare bankruptcy",
        "event type": "Business:Declare-Bankruptcy",
        "keywords": ['bankruptcy', 'bankrupt', 'Bankruptcy'],
        "event description": "The event is related to some organization declaring bankruptcy.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Org} declared bankruptcy.",
        "valid roles": ["Org"],
    },
    "Business.End-Org": {
        "event subtype": "end organization",
        "event type": "Business:End-Org",
        "keywords": ['dissolve', 'disbanded', 'close'],
        "event description": "The event is related to some organization ceasing to exist.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Org} dissolved.",
        "valid roles": ["Org", "Place"],
    },
    "Business.Merge-Org": {
        "event subtype": "merge organization",
        "event type": "Business:Merge-Org",
        "keywords": ['merge', 'merging', 'merger'],
        "event description": "The event is related to two or more organization coming together to form a new organization.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Org} was merged.",
        "valid roles": ["Org"],
    },
    "Business.Start-Org": {
        "event subtype": "start organization",
        "event type": "Business:Start-Org",
        "keywords": ['founded', 'create', 'launch'],
        "event description": "The event is related to a new organization being created.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Agent} launched {ROLE_Org} in {ROLE_Place}.",
        "valid roles": ["Agent", "Org", "Place"],
    },
    "Conflict.Attack": {
        "event subtype": "attack",
        "event type": "Conflict:Attack",
        "keywords": ['war', 'attack', 'terrorism'],
        "event description": "The event is related to conflict and some violent physical act.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Attacker} attacked {ROLE_Target} by {ROLE_Instrument} in {ROLE_Place}.",
        "valid roles": ["Attacker", "Target", "Instrument", "Place"],
    },
    "Conflict.Demonstrate": {
        "event subtype": "demonstrate",
        "event type": "Conflict:Demonstrate",
        "keywords": ['rally', 'protest', 'demonstrate'],
        "event description": "The event is related to a large number of people coming together to protest.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Entity} protested at {ROLE_Place}.",
        "valid roles": ["Entity", "Place"],
    },
    "Contact.Meet": {
        "event subtype": "meet",
        "event type": "Contact:Meet",
        "keywords": ['meeting', 'met', 'summit'],
        "event description": "The event is related to a group of people meeting and interacting with one another face-to-face.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Entity} met at {ROLE_Place}.",
        "valid roles": ["Entity", "Place"],
    },
    "Contact.Phone-Write": {
        "event subtype": "phone write",
        "event type": "Contact:Phone-Write",
        "keywords": ['call', 'communicate', 'e-mail'],
        "event description": "The event is related to people phone calling or messaging one another.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Entity} called or texted messages at {ROLE_Place}.",
        "valid roles": ["Entity", "Place"],
    },
    "Justice.Acquit": {
        "event subtype": "acquit",
        "event type": "Justice:Acquit",
        "keywords": ['acquitted', 'acquittal', 'acquit'],
        "event description": "The event is related to someone being acquitted.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Defendant} was acquitted of the charges by {ROLE_Adjudicator}.",
        "valid roles": ["Defendant", "Adjudicator"],
    },
    "Justice.Appeal": {
        "event subtype": "appeal",
        "event type": "Justice:Appeal",
        "keywords": ['appeal', 'appealing', 'appeals'],
        "event description": "The event is related to someone appealing the decision of a court.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Plaintiff} in {ROLE_Place} appealed the adjudication from {ROLE_Adjudicator}.",
        "valid roles": ["Plaintiff", "Place", "Adjudicator"],
    },
    "Justice.Arrest-Jail": {
        "event subtype": "arrest jail",
        "event type": "Justice:Arrest-Jail",
        "keywords": ['arrest', 'jail', 'detained'],
        "event description": "The event is related to a person getting arrested or a person being sent to jail.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Person} was sent to jailed or arrested by {ROLE_Agent} in {ROLE_Place}.",
        "valid roles": ["Person", "Agent", "Place"],
    },
    "Justice.Charge-Indict": {
        "event subtype": "charge indict",
        "event type": "Justice:Charge-Indict",
        "keywords": ['indict', 'charged', 'accused'],
        "event description": "The event is related to someone or some organization being accused of a crime.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Defendant} was charged by {ROLE_Prosecutor} in {ROLE_Place}, and the adjudication was judged by {ROLE_Adjudicator}.",
        "valid roles": ["Defendant", "Prosecutor", "Place", "Adjudicator"],
    },
    "Justice.Convict": {
        "event subtype": "convict",
        "event type": "Justice:Convict",
        "keywords": ['convicted', 'guilty', 'verdict'],
        "event description": "The event is related to someone being found guilty of a crime.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Defendant} was convicted of a crime in {ROLE_Place}, and the adjudication was judged by {ROLE_Adjudicator}.",
        "valid roles": ["Defendant", "Place", "Adjudicator"],
    },
    "Justice.Execute": {
        "event subtype": "execute",
        "event type": "Justice:Execute",
        "keywords": ['execution', 'executed', 'execute'],
        "event description": "The event is related to someone being executed to death.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Person} was executed by {ROLE_Agent} at {ROLE_Place}.",
        "valid roles": ["Person", "Agent", "Place"],
    },
    "Justice.Extradite": {
        "event subtype": "extradite",
        "event type": "Justice:Extradite",
        "keywords": ['extradition', 'extradited', 'extraditing'],
        "event description": "The event is related to justice. The event occurs when a person was extradited from one place to another place.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Person} was extradicted to {ROLE_Destination} from {ROLE_Origin}, and {ROLE_Agent} was responsible for the extradition.",
        "valid roles": ["Destination", "Origin", "Agent"],
    },
    "Justice.Fine": {
        "event subtype": "fine",
        "event type": "Justice:Fine",
        "keywords": ['fine', 'fined', 'payouts'],
        "event description": "The event is related to someone being issued a financial punishment.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Entity} in {ROLE_Place} was ordered by {ROLE_Adjudicator} to pay a fine.",
        "valid roles": ["Entity", "Place", "Adjudicator"],
    },
    "Justice.Pardon": {
        "event subtype": "pardon",
        "event type": "Justice:Pardon",
        "keywords": ['pardon', 'pardoned', 'remission'],
        "event description": "The event is related to someone being pardoned.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Defendant} received a pardon from {ROLE_Adjudicator}.",
        "valid roles": ["Defendant", "Adjudicator", 'Place'],
    },
    "Justice.Release-Parole": {
        "event subtype": "release parole",
        "event type": "Justice:Release-Parole",
        "keywords": ['parole', 'release', 'free'],
        "event description": "The event is related to an end to someone's custody in prison.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Person} was released by {ROLE_Entity} from {ROLE_Place}.",
        "valid roles": ["Person", "Entity", "Place"],
    },
    "Justice.Sentence": {
        "event subtype": "sentence",
        "event type": "Justice:Sentence",
        "keywords": ['sentenced', 'sentencing', 'sentence'],
        "event description": "The event is related to someone being sentenced to punishment because of a crime.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Defendant} was sentenced to punishment in {ROLE_Place}, and the adjudication was judged by {ROLE_Adjudicator}.",
        "valid roles": ["Defendant", "Place", "Adjudicator"],
    },
    "Justice.Sue": {
        "event subtype": "sue",
        "event type": "Justice:Sue",
        "keywords": ['sue', 'lawsuit', 'suit'],
        "event description": "The event is related to a court proceeding that has been initiated and someone sue the other.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Defendant} was sued by {ROLE_Plaintiff} in {ROLE_Place}, and the adjudication was judged by {ROLE_Adjudicator}.",
        "valid roles": ["Defendant", "Plaintiff", "Place", "Adjudicator"],
    },
    "Justice.Trial-Hearing": {
        "event subtype": "trial hearing",
        "event type": "Justice:Trial-Hearing",
        "keywords": ['trial', 'hearing', 'proceeding'],
        "event description": "The event is related to a trial or hearing for someone.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Defendant}, prosecuted by {ROLE_Prosecutor}, faced a trial in {ROLE_Place}, and the hearing was judged by {ROLE_Adjudicator}.",
        "valid roles": ["Defendant", "Prosecutor", "Place", "Adjudicator"],
    },
    "Life.Be-Born": {
        "event subtype": "born",
        "event type": "Life:Be-Born",
        "keywords": ['born', 'birth', 'bore'],
        "event description": "The event is related to life and someone is given birth to.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Person} was born in {ROLE_Place}.",
        "valid roles": ["Person", "Place"],
    },
    "Life.Die": {
        "event subtype": "die",
        "event type": "Life:Die",
        "keywords": ['kill', 'death', 'assassination'],
        "event description": "The event is related to life and someone died.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Agent} led to {ROLE_Victim} died by {ROLE_Instrument} in {ROLE_Place}.",
        "valid roles": ["Agent", "Victim", "Instrument", "Place"],
    },
    "Life.Divorce": {
        "event subtype": "divorce",
        "event type": "Life:Divorce",
        "keywords": ['divorce', 'divorced', 'Divorce'],
        "event description": "The event is related to life and someone was divorced.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Person} divorced in {ROLE_Place}.",
        "valid roles": ["Person", "Place"],
    },
    "Life.Injure": {
        "event subtype": "injure",
        "event type": "Life:Injure",
        "keywords": ['injure', 'wounded', 'hurt'],
        "event description": "The event is related to life and someone is injured.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Agent} led to {ROLE_Victim} injured by {ROLE_Instrument} in {ROLE_Place}.",
        "valid roles": ["Agent", "Victim", "Instrument", "Place"],
    },
    "Life.Marry": {
        "event subtype": "marry",
        "event type": "Life:Marry",
        "keywords": ['marry', 'marriage', 'married'],
        "event description": "The event is related to life and someone is married.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Person} got married in {ROLE_Place}.",
        "valid roles": ["Person", "Place"],
    },
    "Movement.Transport": {
        "event subtype": "transport",
        "event type": "Movement:Transport",
        "keywords": ['travel', 'go', 'move'],
        "event description": "The event is related to movement. The event occurs when a weapon or vehicle is moved from one place to another.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Artifact} was sent to {ROLE_Destination} from {ROLE_Origin} by {ROLE_Vehicle}, and {ROLE_Agent} was responsible for the transport.",
        "valid roles": ["Artifact", "Destination", "Origin", "Vehicle", "Agent"],
    },
    "Personnel.Elect": {
        "event subtype": "elect",
        "event type": "Personnel:Elect",
        "keywords": ['election', 'elect', 'elected'],
        "event description": "The event is related to a candidate wins an election.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Person} was elected a position, and the election was voted by {ROLE_Entity} in {ROLE_Place}.",
        "valid roles": ["Person", "Entity", "Place"],
    },
    "Personnel.End-Position": {
        "event subtype": "end position",
        "event type": "Personnel:End-Position",
        "keywords": ['former', 'laid off', 'fired'],
        "event description": "The event is related to a person stops working for an organization or a hiring manager.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Person} stopped working for {ROLE_Entity} at {ROLE_Place}.",
        "valid roles": ["Person", "Entity", "Place"],
    },
    "Personnel.Nominate": {
        "event subtype": "nominate",
        "event type": "Personnel:Nominate",
        "keywords": ['named', 'nomination', 'nominate'],
        "event description": "The event is related to a person being nominated for a position.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Person} was nominated by {ROLE_Entity} to do a job.",
        "valid roles": ["Person", "Agent"],
    },
    "Personnel.Start-Position": {
        "event subtype": "start position",
        "event type": "Personnel:Start-Position",
        "keywords": ['hire', 'appoint', 'join'],
        "event description": "The event is related to a person begins working for an organization or a hiring manager.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Person} got new job and was hired by {ROLE_Entity} in {ROLE_Place}.",
        "valid roles": ["Person", "Entity", "Place"],
    },
    "Transaction.Transfer-Money": {
        "event subtype": "transfer money",
        "event type": "Transaction:Transfer-Money",
        "keywords": ['pay', 'donation', 'loan'],
        "event description": "The event is related to transaction. The event occurs when someone is giving, receiving, borrowing, or lending money.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Giver} paid {ROLE_Recipient} in {ROLE_Place}.",
        "valid roles": ["Giver", "Recipient", "Place", "Beneficiary"],
    },
    "Transaction.Transfer-Ownership": {
        "event subtype": "transfer ownership",
        "event type": "Transaction:Transfer-Ownership",
        "keywords": ['sell', 'buy', 'acquire'],
        "event description": "The event is related to transaction. The event occurs when an item or an organization is sold or gave to some other.",
        "ED template": "Event trigger is {Trigger}.",
        "EAE template": "{ROLE_Buyer} got {ROLE_Artifact} from {ROLE_Place} in {ROLE_Place}.",
        "valid roles": ["Buyer", "Artifact", "Seller", "Place", "Beneficiary"],
    },
}

TEMPLATE_ACE_Demo = {"Movement.Transport": "<eg> Given a sentence: Corpsmen quickly <t> take <t> patients by ambulance away from the blowing sand to a triage tent . \nYou need to output: {\"Agent\": \"Corpsmen\", \"Artifact\": \"patients\", \"Vehicle\": \"ambulance\", \"Destination\": \"tent\", \"Origin\": null} <eg>", "Personnel.Elect": "<eg> Given a sentence: BUMPERS Bob , I think that the reason everybody in the south -- you know , first of all , we were -- when Franklin Roosevelt was <t> elected <t> president , we had been living what we thought was still a conquered nation after the Civil War . \nYou need to output: {\"Person\": \"Franklin Roosevelt\", \"Entity\": \"president\", \"Place\": null} <eg>", "Personnel.Start-Position": "<eg> Given a sentence: late word from london that the tabloid the daily mirror just <t> hired <t> peter arnett to be its correspondent in baghdad . \nYou need to output: {\"Place\": \"london\", \"Entity\": \"tabloid\", \"Person\": \"peter arnett\"} <eg>", "Personnel.Nominate": "<eg> Given a sentence: 2003 - 06 - 30 08:11:12 and the pope will reportedly <t> name <t> a new head of the troubled boston archdiocese this week . \nYou need to output: {\"Agent\": \"pope\", \"Person\": \"head\"} <eg>", "Conflict.Attack": "<eg> Given a sentence: in northern iraq , u.s. warplanes <t> hit <t> targets including a ridge east of mosul , where iraqi troops have been entrenched . \nYou need to output: {\"Place\": \"iraq\", \"Attacker\": \"u.s.\", \"Instrument\": \"warplanes\", \"Target\": \"targets\"} <eg>", "Personnel.End-Position": "<eg> Given a sentence: the <t> former <t> governor of basra province also surrendered to coalition forces today . \nYou need to output: {\"Person\": \"governor\", \"Entity\": \"basra province\", \"Place\": \"basra province\"} <eg>", "Contact.Meet": "<eg> Given a sentence: You cite a <t> session <t> you had with President Lyndon Johnson in Austin , I guess , at his ranch , right ? Here is what you quote our President Johnson to you . \nYou need to output: {\"Entity\": \"Lyndon Johnson\", \"Place\": \"ranch\"} <eg>", "Life.Marry": "<eg> Given a sentence: canada is on the path to becoming the third country to allow gay <t> marriage <t> . \nYou need to output: {\"Place\": \"canada\", \"Person\": \"gay\"} <eg>", "Contact.Phone-Write": "<eg> Given a sentence: the 19-year - old army private <t> spoke <t> to her parents yesterday pie phone from a hospital in germany . \nYou need to output: {\"Entity\": \"private,parents\", \"Place\": \"hospital\"} <eg>", "Transaction.Transfer-Money": "<eg> Given a sentence: Of course outspoken organizations such as Planned Parenthood , which <t> gives <t> a lot of money to Democrats , will fight with everything they 've got to keep the Democratic platform as liberal as possible . \nYou need to output: {\"Giver\": \"Planned Parenthood\", \"Beneficiary\": \"Democrats\", \"Recipient\": \"Democrats\", \"Place\": null} <eg>", "Justice.Sue": "<eg> Given a sentence: Larry Klayman , chairman of Judicial Watch , which represent 14 survivors and victims ' relatives who have filed a $ 1.5 billion federal <t> lawsuit <t> against Iraq in Washington , said his organization had served a subpoena on Al - Douri twice , on March 26 and March 28 , but said he has not responded . \nYou need to output: {\"Plaintiff\": \"survivors,relatives\", \"Defendant\": \"Iraq\", \"Place\": \"Washington\", \"Adjudicator\": null} <eg>", "Conflict.Demonstrate": "<eg> Given a sentence: We go to war in Iraq , 200,000 people start <t> protesting <t> in Pakistan , they put too much pressure on the government . \nYou need to output: {\"Entity\": \"people\", \"Place\": \"Pakistan\"} <eg>", "Business.End-Org": "<eg> Given a sentence: Both the AMA and the Bush administration released reports this week saying out of control trial lawyers are <t> driving <t> doctors out of their practices all across the country . \nYou need to output: {\"Place\": \"country\", \"Org\": null} <eg>", "Life.Injure": "<eg> Given a sentence: Earlier Monday , a 19-year - old Palestinian riding a bicycle detonated a 30-kilo ( 66-pound ) bomb near a military jeep in the Gaza Strip , <t> injuring <t> three soldiers . \nYou need to output: {\"Agent\": \"Palestinian\", \"Instrument\": \"bomb\", \"Place\": \"Gaza Strip\", \"Victim\": \"soldiers\"} <eg>", "Life.Die": "<eg> Given a sentence: POLLACK Well , if it 's true and obviously we do n't know just yet but if it 's true , it is very significant because it 's effectively the Iraqis admitting that many of the civilian <t> casualties <t> that we 've seen over the last few days may in fact have been caused by Iraqi surface to air missiles falling back to ground in residential areas . \nYou need to output: {\"Agent\": \"Iraqis\", \"Victim\": \"civilian\", \"Instrument\": \"missiles\", \"Place\": \"areas\"} <eg>", "Justice.Arrest-Jail": "<eg> Given a sentence: DAVID BOWDEN , CNN CORRESPONDENT House clearance Royal Marine style , troops from ( UNINTELLIGIBLE ) commando task to seek out the last pockets of Iraqi resistance in Umm Qasr go in hard to <t> arrest <t> suspected regime sympathizers and search for weapons . \nYou need to output: {\"Agent\": \"troops\", \"Place\": \"Umm Qasr\", \"Person\": \"sympathizers\"} <eg>", "Transaction.Transfer-Ownership": "<eg> Given a sentence: Well , as coalition forces push north , they are encountering a unique problem of combat , getting rid of the weapons <t> captured <t> from the enemy . \nYou need to output: {\"Buyer\": \"forces\", \"Artifact\": \"weapons\", \"Seller\": \"enemy\", \"Place\": null, \"Beneficiary\": null} <eg>", "Justice.Execute": "<eg> Given a sentence: lawyers in texas are trying to keep their client from becoming the 300th person <t> executed <t> in the state since 1982 , when texas resumed capital punishment . \nYou need to output: {\"Person\": \"person\", \"Place\": \"state\", \"Agent\": \"texas\"} <eg>", "Justice.Trial-Hearing": "<eg> Given a sentence: an oklahoma city judge has ruled prosecutors presented enough evidence at a preliminary <t> hearing <t> to try nichols on murder charges for the other 160 victims of the attack . \nYou need to output: {\"Place\": \"oklahoma city\", \"Adjudicator\": \"judge\", \"Prosecutor\": \"prosecutors\", \"Defendant\": \"nichols\"} <eg>", "Justice.Sentence": "<eg> Given a sentence: Malaysia 's second highest court on Friday rejected an appeal by jailed former Deputy Prime Minister Anwar Ibrahim against his conviction and nine - year prison <t> sentence <t> for sodomy . \nYou need to output: {\"Place\": \"Malaysia\", \"Adjudicator\": \"court\", \"Defendant\": \"Anwar Ibrahim\"} <eg>", "Life.Be-Born": "<eg> Given a sentence: Lynn Well , you know , in one sense it is but then , I mean -- well , my grandparents came over , Ellis Island and everything , but when I think about , you know , a foreign person or maybe <t> born <t> in another country and coming here it doe- it does n't seem right in one sense for -- for them to be able to be President of this country . \nYou need to output: {\"Person\": \"person\", \"Place\": \"country\"} <eg>", "Justice.Charge-Indict": "<eg> Given a sentence: The lawyer of former Zambian president Frederick Chiluba was reprimanded by a Lusaka magistrate when his client failed to appear in court on theft <t> charges <t> Friday . \nYou need to output: {\"Prosecutor\": \"magistrate\", \"Defendant\": \"client\", \"Place\": \"court\", \"Adjudicator\": null} <eg>", "Business.Start-Org": "<eg> Given a sentence: A U.S .- sponsored forum that brought Iraqi opposition leaders together to <t> shape <t> the country 's postwar government began Tuesday with a U.S. promise not to rule Iraq and concluded with an agreement to meet again in 10 days . \nYou need to output: {\"Agent\": \"U.S,leaders\", \"Org\": \"government\", \"Place\": \"Iraq\"} <eg>", "Justice.Convict": "<eg> Given a sentence: Malaysia 's second highest court on Friday rejected an appeal by jailed former Deputy Prime Minister Anwar Ibrahim against his <t> conviction <t> and nine - year prison sentence for sodomy . \nYou need to output: {\"Place\": \"Malaysia\", \"Adjudicator\": \"court\", \"Defendant\": \"Anwar Ibrahim\"} <eg>", "Business.Declare-Bankruptcy": "<eg> Given a sentence: worldcom once employed 80,000 people and went broke on the largest corporate <t> bankruptcy <t> in the united states . \nYou need to output: {\"Org\": \"worldcom\", \"Place\": \"united states\"} <eg>", "Justice.Release-Parole": "<eg> Given a sentence: negotiators say he demanded the <t> release <t> of four prisoners , including ramzi binalshibh , a september 11th suspect apprehended last year in pakistan . \nYou need to output: {\"Entity\": \"negotiators\", \"Person\": \"ramzi binalshibh\", \"Place\": null} <eg>", "Justice.Fine": "<eg> Given a sentence: the jury has handed down a $ 30 million , a grand rapids jury saying taco bell has to <t> pay <t> the true creators of the chihuahua mass cot . \nYou need to output: {\"Adjudicator\": \"jury\", \"Entity\": \"taco bell\", \"Place\": null} <eg>", "Justice.Pardon": "<eg> Given a sentence: But after spending 40 days in prison , Jordan 's King Abdullah II <t> pardoned <t> the former legislator known for her harsh criticism of the state . \nYou need to output: {\"Place\": \"Jordan\", \"Adjudicator\": \"Abdullah II\", \"Defendant\": \"legislator\"} <eg>", "Justice.Appeal": "<eg> Given a sentence: in the african nation of nigeria , an islamic court delayed the <t> appeal <t> of a woman condemned to death by stoning . \nYou need to output: {\"Place\": \"nation\", \"Adjudicator\": \"court\", \"Plaintiff\": \"woman\"} <eg>", "Business.Merge-Org": "<eg> Given a sentence: And with the constant <t> merging <t> with other banks , \nYou need to output: {\"Org\": \"banks\"} <eg>", "Justice.Extradite": "<eg> Given a sentence: The waiver of <t> extradition <t> that she signed simply means that if she skips out and goes to another state , she ca n't contest the right of the original court to have her hauled back to its jurisdiction , and that the court wo n't have to initiate the time - consuming process of extraditing her . \nYou need to output: {\"Origin\": \"state\", \"Agent\": \"court\", \"Destination\": \"jurisdiction\"} <eg>", "Life.Divorce": "<eg> Given a sentence: despite prince charles ' ugly <t> divorce <t> with princess di anna , the affection between father and son is now palpable and enviable . \nYou need to output: {\"Person\": \"charles,di anna\", \"Place\": null} <eg>", "Justice.Acquit": "<eg> Given a sentence: The ruling by judges Piet Streicher and Mohamed Navsa of the Supreme Court of Appeal , the highest appeals court in the country , means that Basson can not be tried again and his <t> acquittal <t> stands , the South African Press Association reported . \nYou need to output: {\"Adjudicator\": \"Piet Streicher,Mohamed Navsa\", \"Defendant\": \"Basson\"} <eg>"}

TEMPLATE_ACE = {
    "None": "The word {evt} does not trigger any known event.",
    "Movement.Transport": "The word {evt} triggers a TRANSPORT event: an ARTIFACT (WEAPON or VEHICLE) or a PERSON is moved from one PLACE (GEOPOLITICAL ENTITY, FACILITY, LOCATION) to another.",
    "Personnel.Elect": "The word {evt} triggers an ELECT event which implies an election.",
    "Personnel.Start-Position": "The word {evt} triggers a START-POSITION event: a PERSON elected or appointed begins working for (or changes offices within) an ORGANIZATION or GOVERNMENT.",
    "Personnel.Nominate": "The word {evt} triggers a NOMINATE event: a PERSON is proposed for a position through official channels.",
    "Conflict.Attack": "The word {evt} triggers an ATTACK event: a violent physical act causing harm or damage.",
    "Personnel.End-Position": "The word {evt} triggers an END-POSITION event: a PERSON stops working for (or changes offices within) an ORGANIZATION or GOVERNMENT.",
    "Contact.Meet": "The word {evt} triggers a MEET event: two or more entities come together at a single location and interact with one another face-to-face.",
    "Life.Marry": "The word {evt} triggers a MARRY event: two people are married under the legal definition.",
    "Contact.Phone-Write": "The word {evt} triggers a PHONE-WRITE event: two or more people directly engage in discussion which does not take place 'face-to-face'.",
    "Transaction.Transfer-Money": "The word {evt} triggers a TRANSFER-MONEY event: giving, receiving, borrowing, or lending money when it is NOT in the context of purchasing something. ",
    "Justice.Sue": "The word {evt} triggers a SUE event: a court proceeding has been initiated for the purposes of determining the liability of a PERSON, ORGANIZATION or GEOPOLITICAL ENTITY accused of committing a crime or neglecting a commitment",
    "Conflict.Demonstrate": "The word {evt} triggers a DEMONSTRATE event: a large number of people come together in a public area to protest or demand some sort of official action. For eample: protests, sit-ins, strikes and riots.",
    "Business.End-Org": "The word {evt} triggers an END-ORG event: an ORGANIZATION ceases to exist (in other words, goes out of business).",
    "Life.Injure": "The word {evt} triggers an INJURE event: a PERSON gets/got injured whether it occurs accidentally, intentionally or even self-inflicted.",
    "Life.Die": "The word {evt} triggers a DIE event: a PERSON dies/died whether it occurs accidentally, intentionally or even self-inflicted.",
    "Justice.Arrest-Jail":  "The word {evt} triggers a DIE event: a PERSON is sent to prison.",
    "Transaction.Transfer-Ownership": "The word {evt} triggers a TRANSFER-OWNERSHIP event: The buying, selling, loaning, borrowing, giving, or receiving of artifacts or organizations by an individual or organization.",
    "Justice.Execute": "The word {evt} triggers an EXECUTE event: a PERSON is/was executed",
    "Justice.Trial-Hearing": "The word {evt} triggers a TRIAL-HEARING event: a court proceeding has been initiated for the purposes of determining the guilt or innocence of a PERSON, ORGANIZATION or GEOPOLITICAL ENTITY accused of committing a crime.",
    "Justice.Sentence": "The word {evt} triggers a SENTENCE event:  the punishment for the DEFENDANT is issued",
    "Life.Be-Born": "The word {evt} triggers a BE-BORN event: a PERSON is given birth to.",
    "Justice.Charge-Indict": "The word {evt} triggers a CHARGE-INDICT event: a PERSON, ORGANIZATION or GEOPOLITICAL ENTITY is accused of a crime",
    "Business.Start-Org": "The word {evt} triggers a START-ORG event: a new ORGANIZATION is created.",
    "Justice.Convict": "The word {evt} trigges a CONVICT event: a PERSON, ORGANIZATION or GEOPOLITICAL ENTITY is convicted whenever it has been found guilty of a CRIME.",
    "Business.Declare-Bankruptcy": "The word {evt} triggers a DECLARE-BANKRUPTCY event: an Entity officially requests legal protection from debt collection due to an extremely negative balance sheet.",
    "Justice.Release-Parole": "The word {evt} triggers a RELEASE-PAROLE event.",
    "Justice.Fine": "The word {evt} triggers a FINE event: a GEOPOLITICAL ENTITY, PERSON or ORGANIZATION get financial punishment typically as a result of court proceedings.",
    "Justice.Pardon": "The word {evt} triggers a PARDON event:  a head-of-state or their appointed representative lifts a sentence imposed by the judiciary.",
    "Justice.Appeal": "The word {evt} triggers a APPEAL event: the decision of a court is taken to a higher court for review",
    "Business.Merge-Org": "The word {evt} triggers a MERGE-ORG event: two or more ORGANIZATION Entities come together to form a new ORGANIZATION Entity. ",
    "Justice.Extradite": "The word {evt} triggers a EXTRADITE event.",
    "Life.Divorce": "The word {evt} triggers a DIVORCE event: two people are officially divorced under the legal definition of divorce.",
    "Justice.Acquit": "The word {evt} triggers a ACQUIT event: a trial ends but fails to produce a conviction.",   
}