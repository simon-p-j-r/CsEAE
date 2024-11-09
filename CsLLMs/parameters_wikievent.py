NEW_INSENT_TOKEN = "<t>"
ORD_A = 97


TEMPLATE_WikiEvents_Event = {
    'ArtifactExistence.DamageDestroyDisableDismantle.Damage':"Damager damaged artifact using instrument in place",
    'ArtifactExistence.DamageDestroyDisableDismantle.Destroy':'Destroyer destroyed artifact using instrument in place',
    'ArtifactExistence.DamageDestroyDisableDismantle.DisableDefuse':'Disabler disabled or defused artifact using instrument in place',
    'ArtifactExistence.DamageDestroyDisableDismantle.Dismantle':'Dismantler dismantled artifact using instrument in place',
    'ArtifactExistence.DamageDestroyDisableDismantle.Unspecified':'Damagerdestroyer damaged or destroyed artifact using instrument in place',
    'ArtifactExistence.ManufactureAssemble.Unspecified':'Manufacturer or assembler manufactured or assembled or produced artifact from components using instrument at place',
    'Cognitive.IdentifyCategorize.Unspecified':'Identifier identified object as identifiedRole at place',
    'Cognitive.Inspection.SensoryObserve':'Observer observed entity using instrument in place',
    'Cognitive.Research.Unspecified':'Researcher researched subject using means at place',
    'Cognitive.TeachingTrainingLearning.Unspecified':'TeacherTrainer taught field of knowledge to learner using Means at institution in place',
    'Conflict.Attack.DetonateExplode':'Attacker detonated or exploded explosive device using instrument to attack target at place',
    'Conflict.Attack.Unspecified':'Attacker attacked target using instrument at place',
    'Conflict.Defeat.Unspecified':'Victor defeated defeated in conflict Or election at place',
    'Conflict.Demonstrate.DemonstrateWithViolence':'Demonstrator was in a demonstration involving violence for topic with visual display against target at place, with potential involvement of regulator police or military',
    'Conflict.Demonstrate.Unspecified':'Demonstrator was in a demonstration for topic with visual display against target at place, with potential involvement of regulator police or military',
    'Contact.Contact.Broadcast':'Communicator communicated to recipient about topic using instrument at place (one-way communication)',
    'Contact.Contact.Correspondence':'Participant communicated remotely with participant about topic using instrument at place',
    'Contact.Contact.Meet':'Participant met face-to-face with participant about topic at place',
    'Contact.Contact.Unspecified':'Participant communicated with participant about topic at place (document does not specify in person or not, or one-way or not)',
    'Contact.Prevarication.Unspecified':'Communicator communicated with recipient about topic at place (document does not specify in person or not, or one-way or not)',
    'Contact.RequestCommand.Unspecified':'Communicator communicated with recipient about topic at place (document does not specify in person or not, or one-way or not)',
    'Contact.ThreatenCoerce.Unspecified':'Communicator communicated with recipient about topic at place (document does not specify in person or not, or one-way or not)',
    'Control.ImpedeInterfereWith.Unspecified':'Impeder impeded or interfered with impeded event at place',
    'Disaster.Crash.Unspecified':'Drive or Passenger in vehicle crashed into crash object at place',
    'Disaster.DiseaseOutbreak.Unspecified':'Disease broke out among victims or population at place',
    'Disaster.FireExplosion.Unspecified':'Fire explosion object caught fire or exploded from instrument at place',
    'GenericCrime.GenericCrime.GenericCrime':'Perpetrator committed a crime against victim at place',
    'Justice.Acquit.Unspecified':'Court or judge acquitted defendant of crime in place',
    'Justice.ArrestJailDetain.Unspecified':'Jailer arrested or jailed detainee for crime at place',
    'Justice.ChargeIndict.Unspecified':'Prosecutor charged or indicted defendant before judge or court for crime in place',
    'Justice.Convict.Unspecified':'Judge or court convicted defendant of crime in place',
    'Justice.InvestigateCrime.Unspecified':'Investigator investigated defendant for crime in place',
    'Justice.ReleaseParole.Unspecified':'Judge or court released or paroled defendant from crime in place',
    'Justice.Sentence.Unspecified':'Judge or court sentenced defendant for crime to sentence in place',
    'Justice.TrialHearing.Unspecified':'Prosecutor tried defendant before judge or court for crime in place',
    'Life.Consume.Unspecified':'Consuming entity consumed thing at place',
    'Life.Die.Unspecified':'Victim died at place from medical issue, killed by killer',
    'Life.Illness.Unspecified':'Victim has disease at place, deliberately infected by deliberate injurer',
    'Life.Infect.Unspecified':'Victim was infected with infecting agent from source at place',
    'Life.Injure.Unspecified':'Victim was injured by injurer using instrument in body part with medical condition at place',
    'Medical.Diagnosis.Unspecified':'Treater diagnosed patient with symptom sign for medical condition at place',
    'Medical.Intervention.Unspecified':'Treater treated patient for medical issue with instrument means at place',
    'Medical.Vaccinate.Unspecified':'Treater vaccinated patient via vaccine target for vaccine target at place',
    'Movement.Transportation.Evacuation':'Transporter transported passenger artifact in vehicle from origin place to destination place',
    'Movement.Transportation.IllegalTransportation':'Transporter illegally transported passenger artifact in vehicle from origin place to destination place',
    'Movement.Transportation.PreventPassage':'Preventer prevents transporter from entering destination place from origin place to transport passenger artifact using vehicle',
    'Movement.Transportation.Unspecified':'Transporter transported passenger artifact in vehicle from origin place to destination place',
    'Personnel.EndPosition.Unspecified':'Employee stopped working in position at organization(placeOfEmployment) in place',
    'Personnel.StartPosition.Unspecified':'Employee started working in position at organization(placeOfEmployment) in place',
    'Transaction.Donation.Unspecified':'Giver gave artifact money to recipient for the benefit of beneficiary at place',
    'Transaction.ExchangeBuySell.Unspecified':'Giver bought, sold, or traded acquired entity to recipient in exchange for payment barter for the benefit of beneficiary at place',
}

TEMPLATE_WikiEvents_Event_Demo = {"Cognitive.IdentifyCategorize.Unspecified": "<eg> Given a document: In the hours following the explosions , an array of outlets — including the Associated Press , The Wall Street Journal , and The New York Times — quoted anonymous law enforcement officials who said that police had discovered three and even five additional , unexploded devices around the Boston area . The reports emerged around the same time that , as first reported by The Boston Globe , a bomb squad arranged and detonated a \" controlled explosion \" on Boylston Street , just east of the first two explosions , in order to destroy a cache of \" suspicious packages \" that officials had come across . A similar scene played out in the Boston suburb of Newton , where a bomb squad used a robot to <t> investigate <t> a suspicious object that turned to be a circuit board . Monday night , the Journal quoted law enforcement officials as saying there had been five devices , then updated its report to clarify that \" investigators now doubt the devices were bombs . \" But during Tuesday morning ' s press conference , Massachusetts Governor Deval Patrick announced that law enforcement agents had not in fact discovered any other bombs . \" It ' s important to clarify that two and only two explosive devices were found yesterday . Other parcels have been examined . . . but there were no unexploded bombs , \" he told reporters . The bombs may have been based in pressure cookers \nYou need to output: {\"IdentifiedObject\": \"object\", \"IdentifiedRole\": \"a circuit board\", \"Identifier\": \"squad\", \"Place\": \"Boston\"} <eg>", "Cognitive.Inspection.SensoryObserve": "<eg> Given a document: In the hours following the explosions , an array of outlets — including the Associated Press , The Wall Street Journal , and The New York Times — quoted anonymous law enforcement officials who said that police had discovered three and even five additional , unexploded devices around the Boston area . The reports emerged around the same time that , as first reported by The Boston Globe , a bomb squad arranged and detonated a \" controlled explosion \" on Boylston Street , just east of the first two explosions , in order to destroy a cache of \" suspicious packages \" that officials had come across . A similar scene played out in the Boston suburb of Newton , where a bomb squad used a robot to <t> investigate <t> a suspicious object that turned to be a circuit board . Monday night , the Journal quoted law enforcement officials as saying there had been five devices , then updated its report to clarify that \" investigators now doubt the devices were bombs . \" But during Tuesday morning ' s press conference , Massachusetts Governor Deval Patrick announced that law enforcement agents had not in fact discovered any other bombs . \" It ' s important to clarify that two and only two explosive devices were found yesterday . Other parcels have been examined . . . but there were no unexploded bombs , \" he told reporters . The bombs may have been based in pressure cookers \nYou need to output: {\"Instrument\": \"a robot\", \"ObservedEntity\": \"a circuit board\", \"Observer\": \"squad\", \"Place\": \"Boston\"} <eg>", "Conflict.Attack.Unspecified": "<eg> Given a document: Rightwing rebels No one has claimed responsibility for the alleged assassination attempt outright , though one group – Soldiers Franelas – suggested involvement in a tweet . “ We have shown [ the government ] is vulnerable , ” the group said . “[ The attack ] wasn ’ t achieved today but it is just a matter of time [ until it is ] . ” Little is known about Soldiers Franelas beyond their Twitter presence , where the group regularly posts anti - Maduro tweets . La operación era sobrevolar 2 drones cargados con C4 el objetivo el palco presidencial , francotiradores de la guardia de honor derribaron los drones antes de llegar al objetivo . Demostramos que son vulnerables , no se logró hoy pero es cuestión de tiempo . # MilitaresPatriotas pic . twitter . com / teIEwygN3S — Soldados de Franelas ( @ soldadoDfranela ) August 4 , 2018 The episode on Saturday reminded many in Venezuela of a similar incident last year when Óscar Pérez , a rogue police officer , <t> launched <t> grenades from a stolen helicopter at government buildings in Caracas . Pérez was killed in a shootout six months later . Some analysts suspect Soldiers Franelas of involvement in that incident . A hoax Some observers are suspicious of Maduro ’ s account of events , saying it seems a little too neat in a country where the government has long twisted the truth to its own ends . \nYou need to output: {\"Instrument\": \"grenades\", \"Target\": \"government buildings\", \"Place\": \"Caracas\", \"Attacker\": \"\\u00d3scar P\\u00e9rez\"} <eg>", "Life.Injure.Unspecified": "<eg> Given a document: Police and rescue workers stand at the scene after two assailants had taken five people hostage in the church at Saint - Etienne - du - Rouvray near Rouen in Normandy , France , July 26 , 2016 . A patient shoots at a doctor in a university clinic in Steglitz , a southwestern district of Berlin , before shooting himself . German police say there is no sign of a link to terrorism . July 24 , 2016 - A 21 - year - old Syrian refugee is arrested after killing a pregnant woman and <t> wounding <t> two people with a machete in the southwestern German city of Reutlingen , near Stuttgart . \" Given the current evidence , there is no indication that this was a terrorist attack , \" police say . A special police officer examines the scene after an explosion occurred in Ansbach , Germany , Monday , July 25 , 2016 . A Syrian man wounds 15 people when he blows himself up outside a music festival in Ansbach in southern Germany . Islamic State claims responsibility for the attack . The 27 - year - old arrived in Germany two years ago and claimed asylum . He had been in trouble with the police repeatedly for drug - taking and other offences and had faced deportation to Bulgaria . \nYou need to output: {\"Victim\": \"people\", \"Instrument\": \"machete\", \"Injurer\": \"refugee\", \"BodyPart\": null, \"MedicalCondition\": null, \"Place\": null} <eg>", "Conflict.Attack.DetonateExplode": "<eg> Given a document: image copyright AFP image caption Police called for information on this man after the blast What do we know about the attack ? The explosion struck near the corner of two crowded pedestrian streets in Lyon ' s historic city centre . Investigators have recovered screws , ball bearings , along with a printed circuit , batteries and a remote - controlled trigger device . Denis Broliquier , the city ' s district mayor , told press that \" the charge was too small to kill , \" and a government source told AFP news agency it had been a \" relatively weak explosive charge \" . Those hurt , including a girl aged eight , appear to have suffered superficial injuries . French Interior Minister Christophe Castaner confirmed one of the arrests in a Tweet on Monday , saying joint action by several agencies had been \" decisive \" . No - one has claimed responsibility for the attack . The last time a parcel bomb had exploded in France was in 2007 when a device killed one person and injured another in front of a law office in Paris . Police never found the bomber . Jihadist gun and bomb <t> attacks <t> have killed more than 250 people in France since 2015 and the country remains on high alert , with military patrols a regular feature of security in cities including Lyon . \nYou need to output: {\"Attacker\": \"Jihadist\", \"ExplosiveDevice\": \"bomb\", \"Instrument\": \"gun\", \"Target\": \"people\", \"Place\": \"France\"} <eg>", "Justice.ChargeIndict.Unspecified": "<eg> Given a document: Prosecutors on Tuesday <t> charged <t> Ahmad Khan Rahami , 28 , in federal court in New York in connection with bombings in the Chelsea neighborhood of Manhattan and in New Jersey on Saturday . The federal charges came one day after the police arrested and charged him with several counts , including attempted murder of an officer , after a gunfight in Linden , N . J . , 15 miles from New York City . Here ’ s what else we know : Who is Ahmad Khan Rahami ? Image Images of Mr . Rahami released by the police . Credit . . . New Jersey State Police Mr . Rahami , who previously served time in jail , was born in Afghanistan but is a United States citizen . He lived above the fried chicken restaurant in Elizabeth , N . J . , started by his father , Mohammad , and also worked there . Some of his friends called him Mad — apparently a reference to his first name , not his demeanor — and he was known for an obsession with souped - up Honda Civics that he liked to race . After the bombing , the authorities sent what ’ s being called an unprecedented cellphone alert to area residents , warning of the manhunt for a suspect . Mr . Rahami was found asleep in a doorway of a bar in New Jersey on Monday , and the police were called . \nYou need to output: {\"Prosecutor\": \"Prosecutors\", \"Defendant\": \"Ahmad Khan Rahami\", \"Place\": \"court\", \"JudgeCourt\": \"New York\", \"Crime\": null} <eg>", "Justice.ArrestJailDetain.Unspecified": "<eg> Given a document: An ISIS - inspired Utah teen has been <t> arrested <t> after bringing a homemade bomb to his high school and attempting to detonate it , police said . The student , whose identity was not released , brought the homemade explosive to Pine View High School in St . George inside of his backpack on Monday . An alleged would - be bombing at the 1 , 100 - student school was ultimately thwarted when concerned classmates notified faculty and a school resource officer of the boy ’ s “ suspicious ” backpack that had smoke coming out , cops said . The suspect was arrested after the school was evacuated and authorities , including the bomb squad and FBI , investigated . “ Based on our investigation we can confirm this was a failed attempt to detonate a homemade explosive at the school , ” the St . George Police Department said , adding that after examining the explosive device “ bomb squad members indicted that if it had detonated ; the device had the potential to cause significant injury or death . ” The department noted that “ it was also determined that the male had been researching information and expressing interest in ISIS and promoting the organization . ” Authorities said additional charges may be brought . \nYou need to output: {\"Detainee\": \"teen\", \"Jailer\": \"police\", \"Place\": \"Utah\", \"Crime\": null} <eg>", "Justice.Convict.Unspecified": "<eg> Given a document: Boston Bombing Suspect Found Guilty BOSTON — Dzhokhar Tsarnaev was <t> convicted <t> on all counts Wednesday in the 2013 Boston Marathon bombings by a federal jury that now must decide whether the 21 - year - old former college student should be executed . Jurors spent slightly more than 11 hours deciding Tsarnaev ' s guilt in two days of deliberations after 16 days of testimony . \" It ' s not something that will ever be over , \" said Karen Brassard , whose ankles and shin were injured by pieces of the bomb . \" You ' ll feel it forever . It ' s forever a part of our life . . . . I don ' t know what justice is . I ' m grateful to have him off the street . ' ' Two shrapnel - packed pressure - cooker bombs exploded near the marathon finish line on April 15 , 2013 , killing three people – Martin Richard , 8 , Chinese student Lingzi Lu , 23 , and Krystle Campbell , 29 – and wounding more than 260 others . Tsarnaev also was convicted in the death of Sean Collier , a Massachusetts Institute of Technology patrol officer shot to death three days later , as Tsarnaev and his older brother , Tamerlan , attempted to evade police . \nYou need to output: {\"Defendant\": \"Dzhokhar Tsarnaev\", \"JudgeCourt\": \"jury\", \"Crime\": null, \"Place\": null} <eg>", "Justice.InvestigateCrime.Unspecified": "<eg> Given a document: Transcript for Timeline of the deadly bombings in Texas A string of deadly bombs authorities now <t> investigating <t> if there is a possible serial bomber on the loose in Austin , Texas the first bomb at a package left at a home killing 39 year old Anthony house . The following week to more packages on the same day bolt exploding teenager was killed in a woman badly injured when the device went off her front door . Eight Ford plug detonated next to mistreat any residential subdivision and was triggered . By eight tripwire strung over excellent walk a bomb exploded seriously injuring two minutes the fourth attack in less than twenty days . A fifth bomb exploded Tuesday and it fed ex distribution center but ourself abolished . A female worker with minor injuries and was treated . We just be six bomb which did not detonate eighty different fixed distribution center of the suspected serial bomber Texas . Is now dead after that showdown with a swat team overnight the suspect is a 24 year old white mailing to kill himself blowing themselves while they believe he ' s linked . To six explosive devices that killed two people . This transcript has been automatically generated and may not be 100 % accurate . \nYou need to output: {\"Investigator\": \"authorities\", \"Defendant\": \"bomber\", \"Place\": \"Austin,Texas\", \"Crime\": null} <eg>", "Contact.Contact.Unspecified": "<eg> Given a document: Questions have been raised in recent days about the political and religious beliefs of Tamerlan Tsarnaev , the Boston Marathon bombing suspect killed in a gunfight with police in the early hours of Friday . Anecdotes suggest that Tamerlan became more religious in the last several years and may have embraced more conservative Islamic ideas , although no link has been established between him and any known terrorist group . On Monday , a spokesman for the Islamic Society of Boston , a Cambridge mosque frequented by Tamerlan , <t> contributed <t> to the emerging debate over the suspect ’ s religious beliefs by sharing an anecdote from a January talk at the mosque , during which Tamerlan disrupted the event and insulted the speaker , accusing him of deviating from Islam by comparing the Prophet Muhammad to Martin Luther King Jr . It was the second time that Tamerlan disrupted an event at the mosque because he felt that its religious message was too liberal , said the spokesman , Yusufi Vali , according to a report in The Boston Globe . In disrupting the talk in January at the Islamic Society of Boston mosque in Cambridge , Tamerlan Tsarnaev ’ s shouted at a speaker : “ You are a Kafir ” — a nonbeliever , according to Yusufi Vali , a spokesman for the mosque . Tsarnaev went on to say the speaker was contaminating people ’ s minds and accused him of being a hypocrite . \nYou need to output: {\"Participant\": \"spokesman\", \"Place\": \"Cambridge\", \"Topic\": \"suspect,beliefs\"} <eg>", "Life.Die.Unspecified": "<eg> Given a document: On 10 January 2015 , nine people were <t> killed <t> and more than 30 wounded when two suicide bombers blew themselves up in a crowded café in Jabal Mohsen , Tripoli , Lebanon . == Events == After the first explosion , the second suicide bomber approached the Abu Imran café . Before he could blow himself up , 60 - year - old father of seven \" Abu Ali \" Issa Khaddour rushed and tackled the bomber , and prevented many deaths . The wounded were taken to the hospital in Zgharta , as Jabal Mohsen residents were afraid that Sunni Islamist mobs would kill Alawite wounded if taken to a hospital in Tripoli . The dead were buried on January 12 . The al - Qaeda affiliated terrorist group Nusra Front took responsibility for the attacks , which targeted members of the Alawite sect . It was the first suicide attack on a civilian neighbourhood in nearly a year , following a security sweep that temporarily calmed the Bab al - Tabbaneh – Jabal Mohsen conflict between Sunnis and Alawites of Tripoli . Nusra claimed the attack was in revenge for the Syrian government ' s attacks on Sunnis in the Syrian civil war , and for a bombing of Sunni mosques that was blamed on Alawites . The interior minister of Lebanon , Nohad Machnouk , said on January 11 that the attack was carried out by the Islamic State of Iraq and the Levant . \nYou need to output: {\"Victim\": \"people\", \"Killer\": \"bombers\", \"Place\": \"Jabal Mohsen\", \"MedicalIssue\": null} <eg>", "ArtifactExistence.DamageDestroyDisableDismantle.Damage": "<eg> Given a document: 2 . 48 - Great Northern Railway Station , Gt . Victoria Street . Explosion In a Bedford van which was driven into the station and abandoned in the upper yard . Four buses were completely wrecked and 44 others were damaged . <t> Damage <t> was also caused to the nearby canteen in Murray ' s Tobacco factory . 2 . 50 - Corner of Limestone Road . The explosion was In a hi - jacked car and caused damage to the premises of the Ulster Bank , nearby private houses , and - six cars . Several people were injured . 2 . 50 - York Hotel , Botanic Avenue . The explosion was In a bread van outside the hotel which was badly damaged . The van was blown to pieces . Surrounding property was also damaged and approximately 20 cars suffered . 2 . 55 - Queen Elizabeth Bridge . The explosion was in a Ford car left on the bridge which normally carries heavy traffic , including bus services . Some damage , which was not extensive , was caused to the parapet . 2 . 57 - Liverpool ferry terminus . Explosion in a mini car . Nearby Liverpool Bar extensively damaged . Superficial damage to the terminus itself . \nYou need to output: {\"Artifact\": \"canteen\", \"Place\": \"factory\", \"Damager\": null, \"Instrument\": null} <eg>", "Control.ImpedeInterfereWith.Unspecified": "<eg> Given a document: Fourteen people were killed and 46 wounded by a briefcase bomb that blasted a marketplace in northeastern Armenia on Sunday , the Itar - Tass news agency said Monday . An official with the Noemberyan regional administration earlier said an explosive device had been planted in a briefcase in the village of Bagratashen , a trading point near Armenia ’ s frontier with Georgia and Azerbaijan . Russia ’ s Ostankino television showed wrecked and burned stalls . Fruit and vegetables , some covered in blood , were scattered over a wide area . Armenia and Azerbaijan are locked in a 6 - year - old conflict over the disputed enclave of Nagorno - Karabakh , whose mainly Armenian population seeks independence from Azerbaijan . Advertisement The area where the explosion happened is a center of mafia gangs dealing particularly in black - market fuel , which is in short supply in Armenia because of an <t> embargo <t> imposed by Azerbaijan . \nYou need to output: {\"Impeder\": \"Azerbaijan\", \"Place\": \"Armenia\", \"ImpededEvent\": null} <eg>", "GenericCrime.GenericCrime.GenericCrime": "<eg> Given a document: The government official explained in a press conference that the investigations continue and that , of the 38 linked so far , 31 are deprived of liberty and seven received substitutive measures . Venezuela ’ s Attorney General , Tarek William Saab , informed Tuesday that 38 suspects have been indicted in the case of the frustrated <t> assassination <t> attempt on President Nicolas Maduro , which occurred on Aug . 4 , 2018 . The government official explained in a press conference that the investigations continue and that , of the 38 linked so far , 31 are deprived of liberty and seven received substitutive measures . \" We have taken precautions on this fact to try to streamline the process in terms mandated by law ( . . . ) We hope that Colombia and the United States delivers those people under investigation that fled from Venezuela , \" Saab emphasized , explaining there are 15 prison warrants for suspects that left the country . On Aug . 4 , 2018 , an explosive - loaded drone detonated before reaching a stage where President Maduro was delivering a speech during a military parade in Caracas . At that time , the Venezuelan right - wing opposition and its allies , one of which was the U . S . National Security Advisor John Bolton , said the explosion was \" a montage . \" \nYou need to output: {\"Perpetrator\": \"suspects\", \"Victim\": \"Nicolas Maduro\", \"Place\": null} <eg>", "Movement.Transportation.Unspecified": "<eg> Given a document: DIY Drone Instructable : How To Deliver a Payload Overview These instructions guide you to build a DIY payload delivery drone system that can be mounted on your drone / quadcopter and used to <t> deliver <t> a package to any address . The smart , low - cost delivery solution uses GPS to find its destination and then employs an ultrasonic sensor to measure the ground clearance . Depending on your drone capabilities , this payload system can lift up to 2kg freight . A servo motor is used to release the payload at the desired location . This guide also provides a solution to the sensor integration problem . You can integrate GPS , servo , and ultrasonic sensors without any serial interference . DIY payload delivery drone system Components Breadboard Arduino Mega / Uno Servo motor SG90 Ultrasonic sensor HC - SR04 GPS module NEO - 6M - 001 Connecting wires A bottle cap Glue / Tape Hair pin Breadboard Arduino Mega / Uno Servo motor SG90 Ultrasonic sensor HC - SR04 GPS module NEO - 6M - 001 connecting wires bottle cap hair pin Step 1 : Connecting the Ultrasonic Sensor Take the breadboard and affix the Arduino to its one side , as shown in the picture . Now , take the HC - SR04 ultrasonic sensor and attach it to the lower side of the breadboard . Make the connections as shown in Figure 1 . Connect the pins as follows : \nYou need to output: {\"PassengerArtifact\": \"package\", \"Transporter\": \"your\", \"Vehicle\": \"drone/quadcopter\", \"Destination\": \"address\", \"Origin\": null} <eg>", "Contact.Contact.Broadcast": "<eg> Given a document: Eiffel Tower fenced off to guard against terror attacks Enduring appeal ? The barrier is not expected to dent tourists ' enthusiasm for the iconic site . As many as 7 million people are expected to visit the Eiffel Tower in 2018 . Eiffel Tower fenced off to guard against terror attacks Putting up a barrier The security barrier , which should be completed in mid - July , is also part of a € 300 million revamp of the Eiffel Tower itself . Most of the work is scheduled to be completed ahead of the 2024 Olympic Games in Paris . Eiffel Tower fenced off to guard against terror attacks In the beginning The tower is named after Gustave Eiffel , whose engineering company designed and built the structure from 1887 - 89 . It initially served as the entrance to the World ' s Fair and marked the 100th anniversary of the start of the French Revolution . kw , shs / ng ( AP , AFP , Reuters ) Every evening , DW ' s editors <t> send <t> out a selection of the day ' s hard news and quality feature journalism . You can sign up to receive it directly here \nYou need to output: {\"Communicator\": \"editors\", \"Topic\": \"news\", \"Recipient\": \"You\", \"Place\": \"here\", \"Instrument\": null} <eg>", "ArtifactExistence.DamageDestroyDisableDismantle.Destroy": "<eg> Given a document: In the hours following the explosions , an array of outlets — including the Associated Press , The Wall Street Journal , and The New York Times — quoted anonymous law enforcement officials who said that police had discovered three and even five additional , unexploded devices around the Boston area . The reports emerged around the same time that , as first reported by The Boston Globe , a bomb squad arranged and detonated a \" controlled explosion \" on Boylston Street , just east of the first two explosions , in order to <t> destroy <t> a cache of \" suspicious packages \" that officials had come across . A similar scene played out in the Boston suburb of Newton , where a bomb squad used a robot to investigate a suspicious object that turned to be a circuit board . Monday night , the Journal quoted law enforcement officials as saying there had been five devices , then updated its report to clarify that \" investigators now doubt the devices were bombs . \" But during Tuesday morning ' s press conference , Massachusetts Governor Deval Patrick announced that law enforcement agents had not in fact discovered any other bombs . \" It ' s important to clarify that two and only two explosive devices were found yesterday . Other parcels have been examined . . . but there were no unexploded bombs , \" he told reporters . The bombs may have been based in pressure cookers \nYou need to output: {\"Place\": \"Boylston Street\", \"Destroyer\": \"squad\", \"Artifact\": \"cache\", \"Instrument\": null} <eg>", "Medical.Intervention.Unspecified": "<eg> Given a document: Police are linking the explosion with last Saturday ' s bomb in Brixton which injured 39 people . Responsibility for that bomb has been claimed by four racists groups . Deputy Assistant Commissioner Alan Fry , head of anti - terrorist branch , said : \" The device has similarities to the device that exploded in Brixton with terrible consequences last Saturday . I am linking the crimes . We are treating this as a racist offence . \" Prime Minister Tony Blair , speaking in Washington where he is attending a Nato summit said : \" These things are outrageous and we will not tolerate them and we will make every effort to find out those responsible and bring them to justice . \" A spokesman for The Royal London Hospital at Whitechapel , close to the scene of the explosion , said it had <t> treated <t> five casualties from the blast , two women and three men , all middle - aged . Superintendent David Finnimore said he believed a man was driving the device to Brick Lane police station , a local office closed at weekends , when it went off . Amazingly , the man suffered only slight injuries . The blast destroyed a green Volvo and a maroon Ford Sierra . Police cordoned off the area and evacuated hundreds of people before checking under rows of parked cars in case there were any more devices primed to go off . \nYou need to output: {\"Patient\": \"casualties,women,men\", \"Treater\": \"it\", \"Place\": \"Whitechapel\", \"MedicalIssue\": null, \"Instrument\": null} <eg>", "Conflict.Demonstrate.Unspecified": "<eg> Given a document: AQAP , a media - savvy affiliate of al Qaeda , has produced six issues of \" Inspire \" so far , each featuring praise for martyrs and instructional sections on firearms and explosives for the prospective terrorist . Abdo was charged Friday with the federal crime of possession of a non - registered firearm in addition to previous charges of possession of child pornography and going AWOL from his unit . As he was being led from the courtroom , he yelled out , \" Nidal Hasan ! \" , \" Fort Hood ! \" , and \" 2009 ! \" . READ : Soldier Arrested in Alleged Fort Hood Plot Abdo Went AWOL July 4 Abdo , a Muslim soldier who was in the 101st Airborne Division at Fort Campbell more than 800 miles away in Kentucky , attempted to leave the military in 2010 after <t> protesting <t> the U . S . ' s involvement in Iraq and Afghanistan . In August 2010 he told ABC News he should not have to participate in what he called an \" unjust war \" . \" Any Muslim who knows his religion or maybe takes into account what his religion says can find out very clearly why he should not participate in the U . S . military , \" Abdo said then . READ : Devout Muslim Hopes to Avoid Deployment to Afghanistan \nYou need to output: {\"Target\": \"U.S\", \"Topic\": \"Iraq,Afghanistan\", \"Demonstrator\": \"Abdo\", \"Regulator\": null, \"VisualDisplay\": null, \"Place\": null} <eg>", "Contact.RequestCommand.Broadcast": "<eg> Given a document: 8 . 45 am - Explosion at St . Anthony ’ s Church in Kochchikade , Kotahena , Colombo 8 . 45 am – Explosion at St . Sebastian Catholic Church in Negambo 8 . 45 am – Explosion at Kingsbury Hotel in Colombo 8 . 50 am – Explosion at Cinnamon Grand Hotel in Colombo 9 . 05 am – Explosion at Zion Roman Catholic Church in Batticaloa 11 . 30 am – Emergency Security Council meeting held by Prime Minister Ranil Wickremesinghe 11 . 40 am – Government declares closure of schools across the country for two days 12 . 15 pm – President Maithripala Sirisena <t> appeals <t> for people to keep calm 1 . 45 pm - Explosion at New Tropical Inn in Dehiwela , near the national zoo . This was the seventh explosion . 2 . 15 pm – Explosion at a house in Dematagoda , Colombo , during a police raid ( the eighth explosion ) . Three police officers were killed . 2 . 20 pm – Officials close down the island nation ’ s zoo in Dehiwela . 2 . 30 pm – Government blocks major social media networks and messaging services , such as Facebook and WhatsApp . 2 . 45 pm – Government declares indefinite island wide curfew . 4 . 00 pm – All transport services stopped . 4 . 30 pm – Government declares closure of all state universities indefinitely . \nYou need to output: {\"Communicator\": \"Maithripala Sirisena\", \"Recipient\": \"people\", \"Topic\": null, \"Place\": null} <eg>", "Conflict.Demonstrate.DemonstrateWithViolence": "<eg> Given a document: Venezuela ’ s beleaguered government appeared prepared to go ahead with a vote on Sunday that critics at home and abroad have warned will seal the demise of the oil - rich nation ’ s democracy . At least five people were killed last week after the opposition stepped up its protests against the controversial vote that will elect a 545 - member constituent assembly with the power to rewrite the constitution and dissolve state institutions . A government ban on public demonstrations in the run - up to the election reduced turnouts for nationwide protests called by the opposition , but sporadic looting and <t> clashes <t> between protesters manning barricades of tree branches and barbed wire were reported in several cities on Friday night . Q & A Why is there unrest in Venezuela ? Show • At the heart of the crisis is a cratering economy and acute shortages of medicine and food , coupled with rising anger at a soaring crime rate and an increasingly authoritarian government • The president , Nicolás Maduro , won a general election in 2013 on a platform of continuing his predecessor Hugo Chávez ' s socialist policies of using the country ' s oil riches to reduce inequality and lift people out of poverty , but falling oil prices have forced the government to curtail social programmes • Opposition activists have been staging unrelenting protests against the government . \nYou need to output: {\"Demonstrator\": \"protesters\", \"Regulator\": null, \"VisualDisplay\": null, \"Topic\": null, \"Target\": null, \"Place\": null} <eg>", "Contact.ThreatenCoerce.Unspecified": "<eg> Given a document: The controversial vote comes amid protests that erupted in early April and have since claimed the lives of over 110 people . They followed an unsuccessful attempt of the Venezuelan Supreme Court to absorb the legislative power of the opposition - controlled parliament , the National Assembly . On July 16 , the country ' s opposition has held an unofficial referendum , in which 7 . 2 million people took part and almost 6 . 4 million of them voted against the Constituent Assembly . Venezuela ' s population is estimated at over 31 million people . On Thursday , the Venezuelan government outlawed all protests ahead of a controversial election to the Constituent Assembly until next Tuesday . Still , many people have defied a ban on rallies and took to the streets on Friday night . At least one person died of a gunshot wound he sustained during clashes with law enforcement officers on Friday . The United States <t> warned <t> it would sanction Venezuela and anyone who joins the new legislation body , if Maduro goes through with a July 30 vote . \nYou need to output: {\"Communicator\": \"United States\", \"Recipient\": \"Venezuela,anyone\", \"Topic\": null, \"Place\": null} <eg>", "Contact.Contact.Meet": "<eg> Given a document: The device also had fragments that may have included nails , BBs and ball bearings , the agency said . -- The second bomb was in a metal container , but it was unclear whether it was in a pressure cooker as well , the FBI said . -- Photos obtained by CNN show the remains of a pressure cooker found at the scene , along with a shredded black backpack and what appear to be metal pellets or ball bearings . -- They were sent to the FBI ' s national laboratory in Virginia , where technicians will try to reconstruct the devices . -- In the past , the U . S . government has warned federal agencies that terrorists could turn pressure cookers into bombs by packing them with explosives and shrapnel , and detonating them with blasting caps . -- Authorities sifted through thousands of pieces of evidence and a mass of digital photos and video clips . They have <t> pleaded <t> for the public ' s help in providing additional leads and images . The casualties The blasts left three people dead . -- Martin Richard , an 8 - year - old boy with a gap - tooth grin and bright eyes . He loved to run and play in his yard . -- Krystle Campbell , a 29 - year - old freckle - faced woman described as having \" a heart of gold . \" \nYou need to output: {\"Participant\": \"They,public's\", \"Topic\": \"leads,images\", \"Place\": null} <eg>", "Movement.Transportation.Evacuation": "<eg> Given a document: A police officer stands outside Didsbury mosque in Manchester , May 24 , 2017 . A local imam , Mohammed Saeed , told British newspapers Abedi stopped attending his mosque in 2015 after they argued over IS . “ Salman used to come to the mosque occasionally , he wasn ’ t particularly friendly towards me because he didn ’ t like my anti - IS sermons . He didn ’ t like what I was saying and showed me the face of hate . He came to the mosque less and less after that . ” Son of Libyan emigres Abedi was born in Manchester in 1994 , the third of four children , three boys and one girl . His parents were Libyan emigres who found a home in the northern English city after <t> fleeing <t> the Moammar Gadhafi regime in 1980 . His father , Ramadan Abedi , a former security guard at Manchester Airport , returned to Libya in 2011 to join the uprising against the Libyan autocrat . Since Gadhafi ’ s overthrow his parents spent more time in the North African country than in their home in south Manchester , less than two miles from the scene of Monday ’ s bombing . Police officers arrive at a residential property on Elsmore Road in Fallowfield , Manchester , on May 24 , 2017 , as investigations continue into the May 22 terror attack at the Manchester Arena . \nYou need to output: {\"PassengerArtifact\": \"parents\", \"Origin\": \"Libyan\", \"Destination\": \"city\", \"Transporter\": null, \"Vehicle\": null} <eg>", "Justice.Acquit.Unspecified": "<eg> Given a document: That evening spontaneous protests took place in Madrid , Barcelona , and other cities as demonstrators chanted , “ We want to know the truth before we vote . ” With some 90 percent of Spaniards opposed to Prime Minister José María Aznar ’ s support for the U . S . - led invasion of Iraq , the Islamic connection inevitably put Iraq back on top of the political agenda . This favoured the opposition Spanish Socialist Workers ’ Party ( PSOE ) , which had strongly opposed the war . On March 14 the PSOE scored an upset victory at the polls , and José Luis Rodríguez Zapatero was sworn in as prime minister three days later . In October 2007 , 18 Islamic fundamentalists of mainly North African origin and three Spanish accomplices were convicted of the bombings ( seven others were <t> acquitted <t> ) , which were one of Europe ’ s deadliest terrorist attacks in the years since World War II . \nYou need to output: {\"Defendant\": \"others\", \"JudgeCourt\": null, \"Crime\": null, \"Place\": null} <eg>", "ArtifactExistence.ManufactureAssemble.Unspecified": "<eg> Given a document: DIY Drone Instructable : How To Deliver a Payload Overview These instructions guide you to build a DIY payload delivery drone system that can be <t> mounted <t> on your drone / quadcopter and used to deliver a package to any address . The smart , low - cost delivery solution uses GPS to find its destination and then employs an ultrasonic sensor to measure the ground clearance . Depending on your drone capabilities , this payload system can lift up to 2kg freight . A servo motor is used to release the payload at the desired location . This guide also provides a solution to the sensor integration problem . You can integrate GPS , servo , and ultrasonic sensors without any serial interference . DIY payload delivery drone system Components Breadboard Arduino Mega / Uno Servo motor SG90 Ultrasonic sensor HC - SR04 GPS module NEO - 6M - 001 Connecting wires A bottle cap Glue / Tape Hair pin Breadboard Arduino Mega / Uno Servo motor SG90 Ultrasonic sensor HC - SR04 GPS module NEO - 6M - 001 connecting wires bottle cap hair pin Step 1 : Connecting the Ultrasonic Sensor Take the breadboard and affix the Arduino to its one side , as shown in the picture . Now , take the HC - SR04 ultrasonic sensor and attach it to the lower side of the breadboard . Make the connections as shown in Figure 1 . Connect the pins as follows : \nYou need to output: {\"ManufacturerAssembler\": \"you\", \"Components\": \"DIY payload delivery drone system\", \"Artifact\": \"drone/quadcopter\", \"Instrument\": null, \"Place\": null} <eg>", "ArtifactExistence.DamageDestroyDisableDismantle.Dismantle": "<eg> Given a document: DIY Drone Instructable : How To Deliver a Payload Overview These instructions guide you to build a DIY payload delivery drone system that can be mounted on your drone / quadcopter and used to deliver a package to any address . The smart , low - cost delivery solution uses GPS to find its destination and then employs an ultrasonic sensor to measure the ground clearance . Depending on your drone capabilities , this payload system can lift up to 2kg freight . A servo motor is used to <t> release <t> the payload at the desired location . This guide also provides a solution to the sensor integration problem . You can integrate GPS , servo , and ultrasonic sensors without any serial interference . DIY payload delivery drone system Components Breadboard Arduino Mega / Uno Servo motor SG90 Ultrasonic sensor HC - SR04 GPS module NEO - 6M - 001 Connecting wires A bottle cap Glue / Tape Hair pin Breadboard Arduino Mega / Uno Servo motor SG90 Ultrasonic sensor HC - SR04 GPS module NEO - 6M - 001 connecting wires bottle cap hair pin Step 1 : Connecting the Ultrasonic Sensor Take the breadboard and affix the Arduino to its one side , as shown in the picture . Now , take the HC - SR04 ultrasonic sensor and attach it to the lower side of the breadboard . Make the connections as shown in Figure 1 . Connect the pins as follows : \nYou need to output: {\"Components\": \"payload\", \"Instrument\": \"servo motor\", \"Place\": \"desired location\", \"Dismantler\": null, \"Artifact\": null} <eg>", "Justice.Sentence.Unspecified": "<eg> Given a document: A receipt for Christmas tree lights and surveillance footage showing him buying a pressure cooker from Ikea were also part of the case . The 20 - year - old , who grew up in the well - off suburb Danderyd north of Stockholm , denied the claims , but refused to explain why he bought the ingredients , which can be used to build bombs . \" My opinion is that he acquired , stored and collected liquids and objects to make and then blow up a suicide bomb in order to become a martyr . The criminal act being prepared could seriously have hurt Sweden , \" prosecutor Ewamari Häggkvist said ahead of the verdict . Attunda District Court , north of Stockholm , <t> sentenced <t> him to five years in jail on Thursday morning for \" preparing to commit a terror crime \" . It said it had reduced the sentence by one year because he is aged under 21 . \" It is not clear what would have been the target of a bomb attack . But we believe that blowing up a shrapnel bomb of this kind would have been able to harm Sweden and that the purpose of such a bomb must have been to instil fear in the way referred to by terrorism legislation , \" said the chairman of the court , Mikael Swahn , in a statement . \nYou need to output: {\"JudgeCourt\": \"Attunda District Court\", \"Defendant\": \"him\", \"Place\": \"Stockholm\", \"Crime\": null, \"Sentence\": null} <eg>", "Justice.TrialHearing.Unspecified": "<eg> Given a document: Fighting ' homegrown violent extremists ' The women ’ s arrests show U . S . authorities “ are committed to doing everything in our ability to detect , disrupt and deter attacks by homegrown violent extremists , ' ' U . S . Attorney Loretta Lynch said in a statement . “ As alleged , the defendants in this case carefully studied how to construct an explosive device to launch an attack on the homeland . ' ' In this courtroom sketch , Muhanad Mahmoud Al Farekh , with beard , <t> appears <t> in federal court in New York April 2 , 2015 . Authorities say he planned to kill American soldiers . Their arrests came the same day as another U . S . citizen was brought from Pakistan to New York to face charges he supported a conspiracy to kill Americans . Texas - born Muhanad Mahmoud Al Farekh appeared Thursday in Brooklyn federal court and was held without bail . The women also were held without bail after a brief court appearance , where they spoke only to say they understood the charges against them . Velentzas , 28 , wore a hijab and a dark dress , and Siddiqui , 31 , had on a green T - shirt with a long - sleeved black shirt underneath and a dark long skirt . \nYou need to output: {\"Defendant\": \"Muhanad Mahmoud Al Farekh\", \"Place\": \"courtroom,New York\", \"JudgeCourt\": \"federal court\", \"Prosecutor\": null, \"Crime\": null} <eg>", "Transaction.ExchangeBuySell.Unspecified": "<eg> Given a document: The salesman said the customer <t> bought <t> three 54 - gallon barrels of nitromethane for $ 925 each on Oct . 21 , 1994 , at a drag - car racetrack in Ennis , Texas . Tim Chambers of VP Racing Fuels told jurors the customer had \" kind of like a possum face \" - a description that matches McVeigh . DENVER - A Texas racing fuel salesman - found by the FBI from one of Timothy McVeigh ' s alleged confessions - recalled Monday selling $ 2 , 775 in nitromethane to a customer who claimed to race bikes in Oklahoma City . He remembered the purchase because it was so unusual . \" Well , for one thing , three drums of nitromethane being sold for cash never happens . . . . That does not happen . It did not happen to me . Another thing , somebody comes up to you and they are purchasing three drums and they are going to take it and split it with their friends on nitro . . . Harley bikes , that just doesn ' t happen . \" Harley street bike guys , if they are going to buy gas such as nitromethane from me , they will buy a gallon to five gallons . Now , nitro Harley bikes , you couldn ' t even afford to even put one of those on the street . That just wouldn ' t happen . \" \nYou need to output: {\"Giver\": \"salesman\", \"Recipient\": \"customer\", \"AcquiredEntity\": \"nitromethane\", \"PaymentBarter\": \"54,$925\", \"Beneficiary\": null, \"Place\": null} <eg>", "Movement.Transportation.PreventPassage": "<eg> Given a document: Explosive device hits British diplomatic vehicle in Baghdad , no injuries : embassy BAGHDAD ( Reuters ) - A British diplomatic vehicle was hit by an explosive device on Tuesday on the airport road in Baghdad but no one was injured , the British Embassy in the Iraqi capital Baghdad said . “ We can confirm that one British Embassy Baghdad vehicle was struck by a roadside IED this morning in Baghdad . There were no casualties , ” an embassy spokesperson said . Two security sources , who spoke on condition of anonymity , said the explosion was caused by a homemade explosive device that was planted on the side of the road . Iraqi special forces <t> closed down <t> the road leading to the Green Zone from the western side , they said . Tuesday ’ s attack is the first attack of its kind on a diplomatic convoy along the road for years . Separately on Tuesday , two Katyusha rockets landed inside the Green Zone , which houses government buildings and foreign missions , but caused no casualties or damage , the military said in a statement . Rocket attacks against U . S targets have increased over the past few weeks , with many rockets landing in the vicinity of Baghdad airport or the Green Zone . Last week , in two separate incidents several rockets landed within the perimeter of the airport . Washington blames such attacks on Iranian - backed militia groups . \nYou need to output: {\"Preventer\": \"forces\", \"Destination\": \"Green Zone\", \"Origin\": \"western side\", \"Transporter\": null, \"PassengerArtifact\": null, \"Vehicle\": null} <eg>", "Contact.Contact.Correspondence": "<eg> Given a document: After explosives killed three people and wounded about 180 others during the Boston Marathon , details continue to trickle in as investigators sort through evidence . WHAT ' S NEW -- Obama declared an emergency in Massachusetts and <t> ordered <t> federal aid to supplement state and local response efforts . PREVIOUSLY REPORTED Details on the bombs -- Investigators say the dual bombs , which exploded 12 seconds apart Monday , were designed to deliver vicious suffering . Photos : After the explosion : Moment - by - moment Photos : After the explosion : Moment - by - moment After the explosion : Moment - by - moment – Witness Ben Thorndike saw Monday ' s blast at the Boston Marathon from a nearby office building . His sequence of photos , seven shown here , show the moments immediately after the blast . \nYou need to output: {\"Participant\": \"Obama,federal\", \"Place\": \"Massachusetts\", \"Topic\": \"state\", \"Instrument\": null} <eg>", "Contact.ThreatenCoerce.Broadcast": "<eg> Given a document: \" Any Muslim who knows his religion or maybe takes into account what his religion says can find out very clearly why he should not participate in the U . S . military , \" Abdo said then . READ : Devout Muslim Hopes to Avoid Deployment to Afghanistan The Army approved Abdo ' s request to be discharged as a conscientious objector , but just days later the discharge was put on hold and he was charged with having child pornography on his government - issued computer . Military investigators had been looking at Abdo ' s computer files after he made \" radical statements , \" law enforcement sources told ABC News . After he was told he would face a court martial , Abdo went AWOL from Fort Campbell on July 4 . Though vocal in his protestations against the mission in the Middle East , Abdo did not make any public <t> threats <t> against the military . But when he was discovered Wednesday , Abdo was apparently in the final planning stages of a deadly attack . He was caught in part because a wary local gun store owner called police after Abdo visited the store to buy ammunition and gunpowder . He was acting \" suspicious , \" Guns Galore owner Greg Ebert told ABC News . \" There was clearly something wrong with him , \" Ebert said . \" We made a decision to call the police and fortunately it worked out . \" \nYou need to output: {\"Communicator\": \"Abdo\", \"Recipient\": \"military\", \"Topic\": null, \"Place\": null} <eg>", "Contact.RequestCommand.Unspecified": "<eg> Given a document: A survivor of the deadly 2013 Boston Marathon bombings Thursday described the moments after the attack as \" pure carnage . \" Race spectator Jeff Bauman , who lost both legs in the explosions near the finish line of the race , testified on the second day of the trial of Dzhokhar Tsarnaev in a Boston courthouse . Bauman hobbled to the witness stand on prosthetic legs , then told the jury that he bumped into Tsarnaev ' s older brother Tamerlan along the race course moments before the blasts killed three people and injured another 264 . Defense lawyers sought Thursday to limit graphic testimony of the bombing victims , but Judge George O ' Toole <t> ruled <t> the jury should hear witness descriptions of the aftermath of the attack . Prosecutors allege the Tsarnaevs were trying to avenge U . S . wars in Muslim countries . By blaming the older brother , defense lawyers hope to convince the jury to not sentence Dzhokhar Tsarnaev to death . Dzhokhar Tsarnaev ' s lawyer , Judy Clarke , told the jury Wednesday the 21 - year - old native Chechen participated with Tamerlan in setting off the bombs , but said Tamerlan masterminded the plot and deeply influenced his brother to take part in it . Dzhokhar Tsarnaev inadvertently killed his brother , running over him with a car , as they attempted to elude police days after authorities had identified them as suspects in the bombings . \nYou need to output: {\"Communicator\": \"George O'Toole\", \"Recipient\": \"jury\", \"Topic\": null, \"Place\": null} <eg>", "Conflict.Defeat.Unspecified": "<eg> Given a document: Al Shabaab ’ s Vehicle - Borne IED Campaign : January 2017 – March 2018 Al Shabaab ' s VBIED detonations in Somalia : January 2017 - March 2018 Al Shabaab ’ s vehicle - borne improvised explosive attacks serve as a metric to evaluate the group ’ s ability to disrupt the Somali National Army ( SNA ) and African Union Mission in Somalia ( AMISOM ) forces and threaten the Somali Federal Government ( SFG ) . An ongoing Somali military offensive , backed by the U . S . and an African Union peacekeeping force , has <t> recaptured <t> territory from al Shabaab in south - central Somalia , but has not eliminated al Shabaab ’ s ability to conduct VBIED attacks . [ 1 ] The group uses VBIEDs to breach security installations , often times passing through checkpoints , and conduct high - casualty attacks against government and military personnel . [ 2 ] Outside of Mogadishu , the group uses VBIEDs to gain entry to military bases in order to procure weapons and other supplies and to eliminate AMISOM or Somali government forces from the area , allowing the group to supplant government influence and control populations . [ 3 ] recommended readUS Counterterrorism Objectives in Somalia : Is Mission Failure Likely ? U . S . - backed Somali ground operations along with improved counter - VBIED capabilities among Somali forces may have slightly decreased VBIED attacks between November 2017 and January 2018 . \nYou need to output: {\"Victor\": \"force,military\", \"Defeated\": \"al Shabaab\", \"Place\": \"territory,south-central Somalia\", \"ConflictOrElection\": null} <eg>", "Life.Infect.Unspecified": "<eg> Given a document: Number Crunching The U . S . government claims that civilian casualties caused by drones are in the \" single digits \" during Obama ’ s years in office , while the Stanford - NYU report seeks to establish that there is significant evidence that U . S . drone strikes have killed and <t> injured <t> a larger number of civilians . This is a low bar , and would merely necessitate proving that more than 10 civilians have been killed by drones since Obama assumed office , a claim that has been made by all three major databases aggregating information on drone strikes . The Stanford - NYU report goes further , claiming that between 474 and 881 civilians have been killed since 2004 . However , this does not represent new evidence . Stanford and NYU researchers made no attempt to offer new statistical analysis on the number of civilian casualties caused by drones . Rather , their report is essentially an extended endorsement of a database compiled by The Bureau of Investigative Journalism , a small team of journalists based out of City University , London . In doing so , the report rejects the findings of two other widely cited databases , The Long War Journal , which reports 138 civilian deaths and New America Foundation ’ s Year of the Drone , which lists 152 - 191 civilian deaths and the deaths of 130 - 268 \" unknowns . \" \nYou need to output: {\"Victim\": \"civilians\", \"InfectingAgent\": null, \"Source\": null, \"Place\": null} <eg>", "Cognitive.Research.Unspecified": "<eg> Given a document: The case was originally set in juvenile court last year but was moved to 5th District Court where he was tried as an adult due to the severity of the incident involved . Read more : Judge : 16 - year - old who brought bomb to Pine View High School will be tried as adult The charges stem from a March 5 , 2018 incident in which Farnsworth took a homemade explosive to Pine View High School . He placed the would - be incendiary device in a backpack in the cafeteria area during lunch and left after lighting a fuse . At the time , the cafeteria contained between 75 - 150 students . Pine View High School students are evacuated to the football field as police <t> investigate <t> a bomb scare inside the school and swept the parking lot as a precaution , St . George , Utah , March 5 , 2018 | File photo by Mori Kessler , St . George News Students noticed smoke coming from the backpack that contained the device and reported it to school faculty and the school ’ s resource officer , triggering an evacuation of the school and a multi - agency response from law enforcement . While the incendiary device ’ s fuse fizzled out and failed to ignite , investigators determined that if it had gone off , it would have caused damage to the immediate area and injured those near it . \nYou need to output: {\"Researcher\": \"police\", \"Subject\": \"bomb\", \"Place\": \"school\", \"Means\": null} <eg>", "Disaster.Crash.Unspecified": "<eg> Given a document: \" We showed that the regime is vulnerable . We didn ' t make it , but it ' s a matter of time before we do , \" said Salvatore Lucchese , a former Caracas police chief now in exile . Venezuelan opposition activist Salvatore Lucchese Venezuelan opposition activist Salvatore Lucchese speaks during an interview with Reuters in Bogota , Colombia Aug . 6 , 2018 . Venezuelan opposition activist Salvatore Lucchese speaks during an interview with Reuters in Bogota , Colombia Aug . 6 , 2018 . Lucchese claimed to have been part of the plot in an interview with Reuters this week in which he called for an armed overthrow of Maduro ' s leftist regime . Maduro was addressing a ceremony of the paramilitary National Guard in central Caracas when he came under attack from two drones packed with explosives . The government claims that one of the drones was diverted electronically while the second <t> crashed <t> into a nearby apartment building . Carratu confirmed that Venezuela , a longtime ally of Cuba , has the technology to electronically penetrate and interfere with the electronic signals of aircraft . But he ridiculed claims made on Twitter by persons saying they were involved in the attack that the drones had been shot down with firearms . \" Plastic explosives can ' t be detonated with bullets . They more likely exploded prematurely due to poor preparations by the hit team , \" he said . \nYou need to output: {\"Vehicle\": \"second\", \"Place\": \"apartment building\", \"CrashObject\": \"apartment building\", \"DriverPassenger\": null} <eg>", "ArtifactExistence.DamageDestroyDisableDismantle.Unspecified": "<eg> Given a document: Al Shabaab ’ s Vehicle - Borne IED Campaign : January 2017 – March 2018 Al Shabaab ' s VBIED detonations in Somalia : January 2017 - March 2018 Al Shabaab ’ s vehicle - borne improvised explosive attacks serve as a metric to evaluate the group ’ s ability to disrupt the Somali National Army ( SNA ) and African Union Mission in Somalia ( AMISOM ) forces and threaten the Somali Federal Government ( SFG ) . An ongoing Somali military offensive , backed by the U . S . and an African Union peacekeeping force , has recaptured territory from al Shabaab in south - central Somalia , but has not eliminated al Shabaab ’ s ability to conduct VBIED attacks . [ 1 ] The group uses VBIEDs to <t> breach <t> security installations , often times passing through checkpoints , and conduct high - casualty attacks against government and military personnel . [ 2 ] Outside of Mogadishu , the group uses VBIEDs to gain entry to military bases in order to procure weapons and other supplies and to eliminate AMISOM or Somali government forces from the area , allowing the group to supplant government influence and control populations . [ 3 ] recommended readUS Counterterrorism Objectives in Somalia : Is Mission Failure Likely ? U . S . - backed Somali ground operations along with improved counter - VBIED capabilities among Somali forces may have slightly decreased VBIED attacks between November 2017 and January 2018 . \nYou need to output: {\"Instrument\": \"VBIEDs\", \"DamagerDestroyer\": \"The group\", \"Artifact\": \"installations\", \"Place\": null} <eg>", "Movement.Transportation.IllegalTransportation": "<eg> Given a document: A 40 - year - old Japanese man admitted he landed an unmanned drone in central Tokyo <t> carrying <t> radioactive sand atop Prime Minister Shinzo Abe ' s office to protest nuclear power , police said Saturday . The drone , which had a sign on it saying it was radioactive , was carrying a camera and plastic container with sand contaminated with radioactive cesium , Japanese media said . The police said the radiation was low and did not pose a threat . The stunt initially brought fears of a terrorist attack . Yasuo Yamamoto , who is unemployed , faces a maximum three years in prison if convicted on charges of obstruction of official business . Local media reported that the police said the landing was a protest against nuclear power . Abe is pushing to restart Japan ' s nuclear reactors which are offline in the wake of the Fukushima disaster caused by a tsunami in 2011 . Public broadcaster NHK said the sand the drone was carrying came from an area near the Fukushima meltdown . The drone was discovered Wednesday when new employees were taking a tour of the roof . It was believed to have landed there two weeks ago . “ I was operating the drone around 3 : 30 in the morning on April 9 to express my opposition to nuclear power generation , ” police quoted the alleged drone operator as saying . \nYou need to output: {\"Vehicle\": \"unmanned drone\", \"Destination\": \"office\", \"PassengerArtifact\": \"radioactive sand\", \"Transporter\": \"man\", \"Origin\": null} <eg>", "Contact.ThreatenCoerce.Correspondence": "<eg> Given a document: Indonesian Police Receive Terrorist Threat Targeting Bali JAKARTA — In Indonesia there are growing concerns that more deadly attacks could follow last week ’ bombings in Jakarta by Islamist militants . Bali police Tuesday say they received an anonymous letter warning that the resort Island will be the next target for a terrorist assault . \" The letter was <t> sent <t> by an anonymous individual to Buleleng district , and the police are still conducting an investigation , and trying to find out who sent the letter . But again , I urge people in Bali not to be afraid , but they should stay alert , \" said Bali Police Chief Sugeng Priyanto . Authorities say they ' ve increased security at shopping malls and other locations that draw crowds in Bali . In 2002 , the popular resort island was targeted by Jemaah Islamiyah ( JI ) , an Indonesia - based terrorist group with links to al - Qaida . The bombing of a club in Bali killed 202 people , mostly foreigners . The Bali bombing severely hurt Indonesia ’ s tourism industry , and began a decade of deadly plots in Indonesia carried out by Southeast Asian militants affiliated with al - Qaida . Indonesia successfully combated the JI related terrorist threat through police action , intelligence operations and high profile criminal prosecutions . \nYou need to output: {\"Communicator\": \"individual\", \"Recipient\": \"Buleleng district\", \"Topic\": null, \"Place\": null} <eg>", "Personnel.EndPosition.Unspecified": "<eg> Given a document: In August 2010 he told ABC News he should not have to participate in what he called an \" unjust war \" . \" Any Muslim who knows his religion or maybe takes into account what his religion says can find out very clearly why he should not participate in the U . S . military , \" Abdo said then . READ : Devout Muslim Hopes to Avoid Deployment to Afghanistan The Army approved Abdo ' s request to be <t> discharged <t> as a conscientious objector , but just days later the discharge was put on hold and he was charged with having child pornography on his government - issued computer . Military investigators had been looking at Abdo ' s computer files after he made \" radical statements , \" law enforcement sources told ABC News . After he was told he would face a court martial , Abdo went AWOL from Fort Campbell on July 4 . Though vocal in his protestations against the mission in the Middle East , Abdo did not make any public threats against the military . But when he was discovered Wednesday , Abdo was apparently in the final planning stages of a deadly attack . He was caught in part because a wary local gun store owner called police after Abdo visited the store to buy ammunition and gunpowder . He was acting \" suspicious , \" Guns Galore owner Greg Ebert told ABC News . \nYou need to output: {\"Employee\": \"Abdo\", \"PlaceOfEmployment\": \"Army\", \"Position\": null, \"Place\": null} <eg>", "ArtifactExistence.DamageDestroyDisableDismantle.DisableDefuse": "<eg> Given a document: 270p | 6 . 3MB 360p | 9 . 9MB 720p | 56 . 3MB Other bombs The FBI wants to question Rahami about another bombing Saturday morning in Seaside Park , New Jersey , south of New York , that forced the cancellation of a charity road race . No one was injured . Other bombs were found in a garbage can at a train station Sunday morning in Elizabeth , New Jersey . One of the bombs exploded while a robot was trying to <t> disarm <t> it . Again , no one was hurt . FILE - Federal Bureau of Investigation ( FBI ) officials label and collect evidence near the site of an explosion which took place on Saturday night in the Chelsea neighborhood of Manhattan , New York , Sept . 18 , 2016 . Rahami ' s alleged motive for the bombings is unknown . New York City Mayor Bill de Blasio said Rahami is the only suspect so far . The mayor on Monday said there is every reason to believe the bombings were acts of terrorism , and the FBI is looking for any links to foreign terror groups . Obama : We have to be vigilant Speaking in New York , President Barack Obama said the investigation is moving rapidly and that everyone is working together to get to the bottom of what happened . He said terrorists and extremists want to hurt innocent people , inspire fear and disrupt life . \nYou need to output: {\"Instrument\": \"robot\", \"Artifact\": \"bombs\", \"Disabler\": null, \"Place\": null} <eg>", "Personnel.StartPosition.Unspecified": "<eg> Given a document: The attacks on the Birmingham pubs , neither of which had any military connection , “ went against everything we claimed to stand for , ” he said . The bombings came after police disrupted the funeral arrangements for James McDade , a lieutenant in the Birmingham Brigade of the IRA who blew himself up while trying to attack Coventry Telephone Exchange a few days earlier . “ Tempers were high and I , for one , certainly at first feared that the local IRA had knowingly caused these dreadful casualties , ” said Conway . He claimed the IRA unit responsible “ could not find a functioning telephone box , so they were unable to issue a warning sufficiently in time to clear the bars and prevent the mass loss of life . ” Conway finally left the Republican movement in 1993 and <t> is <t> now a criminal lawyer in Dublin . Fighting families ’ legal aid problems still to be resolved Relatives of more than half the victims are hoping to be represented by lawyers at the pre - inquest review hearing on Thursday . But at the time of going to press , longstanding issues of legal aid had still to be resolved . For several months the Government had insisted that KRW Law , the Belfast - based law firm representing most of the families , was not eligible for legal aid . \nYou need to output: {\"Employee\": \"Conway\", \"PlaceOfEmployment\": \"Dublin\", \"Position\": null, \"Place\": null} <eg>", "Cognitive.TeachingTrainingLearning.Unspecified": "<eg> Given a document: Lived in Britain The last few years Zaghba lived in Britain , where he worked on and off at a restaurant and a hotel near Regents Park , traveling back and forth to visit his mother , who lives in Bologna . The naming of the third Islamic militant came after it emerged earlier Tuesday that the ringleader of Saturday ’ s attack , 27 - year - old British - Pakistani Khuram Shazad Butt worked for a man accused of helping to <t> train <t> the Islamic extremists responsible for the July 7 , 2005 underground train bombings in London , Britain ’ s first Islamist suicide attack . Fifty - two people were killed across Britain ’ s capital in the coordinated strike and more than 700 others were injured . This is undated three photo combo handout photo issued by the Metropolitan Police on Tuesday June 6 , 2017 of Khuram Shazad Butt , left , Rachid Redouane , centre and Youssef Zaghba who have been named as the suspects in Saturday ' s attack at London Bridge . Counterterror analysts say they are surprised that Butt remained a \" low priority \" for the security services despite his close connections to Sajeel Shahid , a 41 - year - old who ran an all - Muslin gym in east London and was named in a New York court case as having helped to set up weapons training in Pakistan for the July 7 suicide bombers . \nYou need to output: {\"Learner\": \"extremists\", \"TeacherTrainer\": null, \"FieldOfKnowledge\": null, \"Means\": null, \"Institution\": null, \"Place\": null} <eg>", "Justice.ReleaseParole.Unspecified": "<eg> Given a document: HOUSTON – A 26 - year - old man has been sentenced to federal prison following his conviction for attempting to maliciously damage property receiving federal financial assistance , announced U . S . Attorney Ryan K . Patrick . Andrew Schneck pleaded guilty March 27 , 2018 . Today , U . S . District Judge Ewing Werlein Jr . handed Schneck a 78 - month sentence to be immediately followed by three years of supervised <t> release <t> . The court also imposed a $ 10 , 000 fine . On the evening of Aug . 19 , 2017 , a Houston park ranger observed Schneck kneeling among the bushes in front of the General Dowling Monument located in Hermann Park in Houston . Schneck was holding two small boxes with various items inside to include what appeared to be duct tape and wires . After placing the boxes on the ground per the ranger ’ s request , Schneck took a drink of clear liquid from a plastic bottle , spit it out and poured the remainder on the ground . The ranger then noticed a timer and wires in the box and notified the Houston Police Department ( HPD ) . \nYou need to output: {\"Defendant\": \"Schneck\", \"JudgeCourt\": \"Ewing Werlein Jr.\", \"Crime\": null, \"Place\": null} <eg>", "Transaction.Donation.Unspecified": "<eg> Given a document: The Tsarnaev brothers visit the Manchester Line Firing Range in N . H . a month before the bombing . Share Email to a Friend Embed The Tsarnaev brothers visit the Manchester Line Firing Range in N . H . a month before the bombing . March 30 , 2013 Tamerlan Tsarnaev also bought a screwdriver and soldering gun from Home Depot in Somerville , April 8 , 2013 Tamerlan bought remote - control car devices from RC Cars in Malden , which prosecutors say are related to the equipment needed by the Tsarnaevs to remotely trigger the bombs . April 13 , 2013 Tamerlan Tsarnaev purchases ammunition from a store in New Hampshire and <t> sends <t> $ 900 in cash through Moneygram to his and Dzhokhar ’ s mother , Zubeidat , through a location in Somerville . April 14 , 2013 Dzhokhar Tsarnaev opens a prepaid cellphone account under the name Jahar Tsarni . He would use this phone while at the Boston Marathon the next day . On the same day , Tamerlan Tsarnaev buys two backpacks at a Target in Watertown that were used to carry the bombs . Federal Public Defender Office April 15 , 2013 At about 2 : 50 p . m . , two homemade pressure - cooker bombs are detonated remotely by the Tsarnaevs near the finish line of the Boston Marathon , killing three and injuring some 260 others . Seventeen people lost limbs . April 15 , 2013 \nYou need to output: {\"Recipient\": \"Zubeidat\", \"Giver\": \"Tamerlan Tsarnaev\", \"ArtifactMoney\": \"$900\", \"Beneficiary\": null, \"Place\": null} <eg>", "Disaster.DiseaseOutbreak.Unspecified": "<eg> Given a document: But the Medical Federation of Venezuela has come out in support of Sarmiento . “ How long will this routine go on ? Every time someone tells this government the truth in connection with a disease , an economic problem or a security issue , that person automatically becomes a coup - plotter , ” said Douglas Nátera , president of the federation . Health Minister Nancy Pérez , who has held that portfolio for just a few days , made a public statement on Wednesday to address the growing social alarm . “ The main thing is that there is no strange virus right now . The moment some <t> disease <t> crops up , the people of Venezuela will know about it , because it is not state policy to conceal information but rather to disclose it and to take the necessary measures . ” For every patient diagnosed with Chikungunya , there could be as many as 1 , 000 more Yet the minister admitted to 45 , 745 confirmed cases of dengue fever and 398 more of the Chikungunya virus , which causes acute joint pains and is also spread by mosquitoes . Another 1 , 200 patients are under observation . But Rafael Arreaza , a surgeon and former director of Venezuela ’ s Social Security service , questioned the minister ’ s figures and filed a complaint against the government with the Ombudsman . \nYou need to output: {\"Place\": \"Venezuela\", \"Victim\": \"people\", \"Disease\": null} <eg>"}
TEMPLATE_WikiEvents_Event_Full = {
    'ArtifactExistence.DamageDestroyDisableDismantle.Damage':'Damager damaged Artifact using Instrument in Place',
    'ArtifactExistence.DamageDestroyDisableDismantle.Destroy':'Destroyer destroyed Artifact using Instrument in Place',
    'ArtifactExistence.DamageDestroyDisableDismantle.DisableDefuse':'Disabler disabled or defused Artifact using Instrument in Place',
    'ArtifactExistence.DamageDestroyDisableDismantle.Dismantle':'Dismantler dismantled Artifact using Instrument from Components in Place',
    'ArtifactExistence.DamageDestroyDisableDismantle.Unspecified':'DamagerDestroyer damaged or destroyed Artifact using Instrument in Place',
    'ArtifactExistence.ManufactureAssemble.Unspecified':'ManufacturerAssembler manufactured or assembled or produced Artifact from Components using Instrument at Place',
    'Cognitive.IdentifyCategorize.Unspecified':'Identifier identified IdentifiedObject as IdentifiedRole at Place',
    'Cognitive.Inspection.SensoryObserve':'Observer observed ObservedEntity using Instrument in Place',
    'Cognitive.Research.Unspecified':'Researcher researched Subject using Means at Place',
    'Cognitive.TeachingTrainingLearning.Unspecified':'TeacherTrainer taught FieldOfKnowledge to Learner using Means at Institution in Place',
    'Conflict.Attack.DetonateExplode':'Attacker detonated or exploded ExplosiveDevice using Instrument to attack Target at Place',
    'Conflict.Attack.Unspecified':'Attacker attacked Target using Instrument at Place',
    'Conflict.Defeat.Unspecified':'Victor Defeated in ConflictOrElection at Place',
    'Conflict.Demonstrate.DemonstrateWithViolence':'Demonstrator was in a demonstration involving violence for Topic with VisualDisplay against Target at Place, with potential involvement of Regulator police or military',
    'Conflict.Demonstrate.Unspecified':'Demonstrator was in a demonstration for Topic with VisualDisplay against Target at Place, with potential involvement of Regulator police or military',
    'Contact.Contact.Broadcast':'Communicator communicated to Recipient about Topic using Instrument at Place (one-way communication)',
    'Contact.Contact.Correspondence':'Participant communicated remotely with Participant about Topic using Instrument at Place',
    'Contact.Contact.Meet':'Participant met face-to-face with Participant about Topic at Place',
    'Contact.Contact.Unspecified':'Participant communicated with Participant about Topic at Place (document does not specify in person or not, or one-way or not)',
    'Contact.Prevarication.Unspecified':'Communicator communicated with Recipient about Topic at Place (document does not specify in person or not, or one-way or not)',
    'Contact.RequestCommand.Unspecified':'Communicator communicated with Recipient about Topic at Place (document does not specify in person or not, or one-way or not)',
    'Contact.RequestCommand.Broadcast':'Communicator communicated with Recipient about Topic at Place (document does not specify in person or not, or one-way or not)',
    'Contact.RequestCommand.Correspondence':'Communicator communicated with Recipient about Topic at Place (document does not specify in person or not, or one-way or not)',
    'Contact.RequestCommand.Meet':'Communicator communicated with Recipient about Topic at Place (document does not specify in person or not, or one-way or not)',
    'Contact.ThreatenCoerce.Unspecified':'Communicator communicated with Recipient about Topic at Place (document does not specify in person or not, or one-way or not)',
    'Contact.ThreatenCoerce.Broadcast':'Communicator communicated with Recipient about Topic at Place (document does not specify in person or not, or one-way or not)',
    'Contact.ThreatenCoerce.Correspondence':'Communicator communicated with Recipient about Topic at Place (document does not specify in person or not, or one-way or not)',
    'Control.ImpedeInterfereWith.Unspecified':'Impeder impeded or interfered with ImpededEvent at Place',
    'Disaster.Crash.Unspecified':'DriverPassenger in Vehicle crashed into CrashObject at Place',
    'Disaster.DiseaseOutbreak.Unspecified':'Disease broke out among Victim or population at Place',
    'Disaster.FireExplosion.Unspecified':'FireExplosionObject caught fire or exploded from Instrument at Place',
    'GenericCrime.GenericCrime.GenericCrime':'Perpetrator committed a crime against Victim at Place',
    'Justice.Acquit.Unspecified':'JudgeCourt acquitted Defendant of Crime in Place',
    'Justice.ArrestJailDetain.Unspecified':'Jailer arrested or jailed Detainee for Crime at Place',
    'Justice.ChargeIndict.Unspecified':'Prosecutor charged or indicted Defendant before JudgeCourt for Crime in Place',
    'Justice.Convict.Unspecified':'JudgeCourt convicted Defendant of Crime in Place',
    'Justice.InvestigateCrime.Unspecified':'Investigator investigated Defendant for Crime in Place',
    'Justice.ReleaseParole.Unspecified':'JudgeCourt released or paroled Defendant from Crime in Place',
    'Justice.Sentence.Unspecified':'JudgeCourt sentenced Defendant for Crime to Sentence in Place',
    'Justice.TrialHearing.Unspecified':'Prosecutor tried Defendant before JudgeCourt for Crime in Place',
    'Life.Consume.Unspecified':'ConsumingEntity consumed ConsumedThing at Place',
    'Life.Die.Unspecified':'Victim died at Place from MedicalIssue, killed by Killer',
    'Life.Illness.Unspecified':'Victim has Disease sickness or illness at Place, deliberately infected by DeliberateInjurer',
    'Life.Infect.Unspecified':'Victim was infected with InfectingAgent from Source at Place',
    'Life.Injure.Unspecified':'Victim was injured by Injurer using Instrument in BodyPart with MedicalCondition at Place',
    'Medical.Diagnosis.Unspecified':'Treater diagnosed Patient with SymptomSign for MedicalCondition at Place',
    'Medical.Intervention.Unspecified':'Treater treated Patient for MedicalIssue with Instrument Means at Place',
    'Medical.Vaccinate.Unspecified':'Treater vaccinated Patient via VaccineMethod for VaccineTarget at Place',
    'Movement.Transportation.Evacuation':'Transporter transported PassengerArtifact in Vehicle from Origin Place to Destination Place',
    'Movement.Transportation.IllegalTransportation':'Transporter illegally transported PassengerArtifact in Vehicle from Origin Place to Destination Place',
    'Movement.Transportation.PreventPassage':'Preventer prevents Transporter from entering Destination Place from Origin Place to transport PassengerArtifact using Vehicle',
    'Movement.Transportation.Unspecified':'Transporter transported PassengerArtifact in Vehicle from Origin Place to Destination Place',
    'Personnel.EndPosition.Unspecified':'Employee stopped working in Position at PlaceOfEmployment organization in Place',
    'Personnel.StartPosition.Unspecified':'Employee started working in Position at PlaceOfEmployment organization in Place',
    'Transaction.Donation.Unspecified':'Giver gave ArtifactMoney to Recipient for the benefit of Beneficiary at Place',
    'Transaction.ExchangeBuySell.Unspecified':'Giver bought, sold, or traded AcquiredEntity to Recipient in exchange for PaymentBarter for the benefit of Beneficiary at Place',
}
  
TEMPLATE_WikiEvents_All = {
  "ArtifactExistence.DamageDestroyDisableDismantle.Damage": {
    "event_id": "LDC_KAIROS_evt_001",
    "template": "<arg1> damaged <arg2> using <arg3> instrument in <arg4> place",
    "i-label": 1,
    "keywords": [
      "damage",
      "harm"
    ],
    "roles": [
      "Damager",
      "Artifact",
      "Instrument",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "bal",
        "com",
        "fac",
        "loc",
        "mon",
        "nat",
        "pth",
        "veh",
        "wea"
      ],
      [
        "com",
        "veh",
        "wea"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Contact.RequestCommand.Broadcast": {
        "i-label": 111111,

        "roles": [
            "Communicator",
            "Recipient",
            "Topic",
            "Place"
        ],
    },
  "Contact.RequestCommand.Correspondence": {
        "i-label": 111111,

        "roles": [
            "Communicator",
            "Recipient",
            "Topic",
            "Place"
        ],
    },
  "Contact.RequestCommand": {
    "i-label": 111111,

    "roles": [
        "Communicator",
        "Recipient",
        "Topic",
        "Place"
    ],
},
  "Contact.ThreatenCoerce.Broadcast": {
    "i-label": 111111,

    "roles": [
        "Communicator",
        "Recipient",
        "Topic",
        "Place"
    ],
},
  "Contact.ThreatenCoerce.Correspondence": {
        "i-label": 111111,

        "roles": [
            "Communicator",
            "Recipient",
            "Topic",
            "Place"
        ],
    },
  "ArtifactExistence.DamageDestroyDisableDismantle.Destroy": {
    "event_id": "LDC_KAIROS_evt_002",
    "template": "<arg1> destroyed <arg2> using <arg3> instrument in <arg4> place",
    "i-label": 2,
    "keywords": [
      "destroy",
      "destruct",
      "sabotage"
    ],
    "roles": [
      "Destroyer",
      "Artifact",
      "Instrument",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "bal",
        "com",
        "fac",
        "loc",
        "mon",
        "nat",
        "pth",
        "veh",
        "wea"
      ],
      [
        "com",
        "veh",
        "wea"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "ArtifactExistence.DamageDestroyDisableDismantle.DisableDefuse": {
    "event_id": "LDC_KAIROS_evt_003",
    "template": "<arg1> disabled or defused <arg2> using <arg3> instrument in <arg4> place",
    "i-label": 3,
    "keywords": [
      "disable",
      "defuse",
      "deactivate"
    ],
    "roles": [
      "Disabler",
      "Artifact",
      "Instrument",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "abs",
        "com",
        "fac",
        "veh",
        "wea"
      ],
      [
        "abs",
        "com",
        "veh",
        "wea"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "ArtifactExistence.DamageDestroyDisableDismantle.Dismantle": {
    "event_id": "LDC_KAIROS_evt_004",
    "template": "<arg1> dismantled <arg2> using <arg3> instrument in <arg4> place",
    "i-label": 4,
    "keywords": [
      "dismantle",
      "disassemble",
      "deconstruct"
    ],
    "roles": [
      "Dismantler",
      "Artifact",
      "Instrument",
      "Components",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "com",
        "fac",
        "veh",
        "wea"
      ],
      [
        "com",
        "veh"
      ],
      [
        "com"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "ArtifactExistence.DamageDestroyDisableDismantle.Unspecified": {
    "event_id": "LDC_KAIROS_evt_005",
    "template": "<arg1> damaged or destroyed <arg2> using <arg3> instrument in <arg4> place",
    "i-label": 5,
    "keywords": [
      "demolish",
      "ruin",
      "devastate",
      "disrupt",
      "wreck"
    ],
    "roles": [
      "DamagerDestroyer",
      "Artifact",
      "Instrument",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "bal",
        "com",
        "fac",
        "loc",
        "mon",
        "nat",
        "pth",
        "veh",
        "wea"
      ],
      [
        "com",
        "veh",
        "wea"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "ArtifactExistence.ManufactureAssemble.Unspecified": {
    "event_id": "LDC_KAIROS_evt_006",
    "template": "<arg1> manufactured or assembled or produced <arg2> from <arg3> components using <arg4> at <arg5> place",
    "i-label": 6,
    "keywords": [
      "build",
      "assemble",
      "manufacture"
    ],
    "roles": [
      "ManufacturerAssembler",
      "Artifact",
      "Components",
      "Instrument",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "bal",
        "com",
        "fac",
        "mon",
        "veh",
        "wea",
        "pth"
      ],
      [
        "com",
        "veh",
        "wea",
        "pth"
      ],
      [
        "com",
        "inf"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Cognitive.IdentifyCategorize.Unspecified": {
    "event_id": "LDC_KAIROS_evt_007",
    "template": "<arg1> identified <arg2> as <arg3> at <arg4> place",
    "i-label": 7,
    "keywords": [
      "identify",
      "recognize",
      "discover"
    ],
    "roles": [
      "Identifier",
      "IdentifiedObject",
      "IdentifiedRole",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "event",
        "per",
        "org",
        "bal",
        "com",
        "fac",
        "loc",
        "mon",
        "veh",
        "wea",
        "aml",
        "bod",
        "nat",
        "pla",
        "pth"
      ],
      [
        "event",
        "per",
        "org",
        "bal",
        "com",
        "fac",
        "loc",
        "mon",
        "veh",
        "wea",
        "aml",
        "bod",
        "nat",
        "pla",
        "pth"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Cognitive.Inspection.SensoryObserve": {
    "event_id": "LDC_KAIROS_evt_008",
    "template": "<arg1> observed <arg2> using <arg3> in <arg4> place",
    "i-label": 8,
    "keywords": [
      "observe",
      "inspect",
      "examine"
    ],
    "roles": [
      "Observer",
      "ObservedEntity",
      "Instrument",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid",
        "com",
        "veh",
        "wea",
        "fac",
        "bal",
        "mon",
        "mhi",
        "aml",
        "bod",
        "nat",
        "pla",
        "pth",
        "event"
      ],
      [
        "com"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Cognitive.Research.Unspecified": {
    "event_id": "LDC_KAIROS_evt_009",
    "template": "<arg1> researched <arg2> subject using <arg3> at <arg4> place",
    "i-label": 9,
    "keywords": [
      "research",
      "analyze",
      "probe"
    ],
    "roles": [
      "Researcher",
      "Subject",
      "Means",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "event",
        "per",
        "org",
        "gpe",
        "sid",
        "loc",
        "fac",
        "veh",
        "wea",
        "com",
        "bal",
        "mon",
        "law",
        "res",
        "val",
        "mhi",
        "inf",
        "abs",
        "aml",
        "bod",
        "nat",
        "pla",
        "pth"
      ],
      [
        "event",
        "abs",
        "inf",
        "com"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Cognitive.TeachingTrainingLearning.Unspecified": {
    "event_id": "LDC_KAIROS_evt_010",
    "template": "<arg1> taught <arg2> field of knowledge to <arg3> using <arg4> at <arg5> institution in <arg6> place",
    "i-label": 10,
    "keywords": [
      "learn",
      "teach",
      "train",
      "school",
      "lessons",
      "classes"
    ],
    "roles": [
      "TeacherTrainer",
      "FieldOfKnowledge",
      "Learner",
      "Means",
      "Institution",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "aml"
      ],
      [
        "inf"
      ],
      [
        "per",
        "org",
        "com",
        "aml",
        "abs"
      ],
      [
        "com",
        "abs",
        "inf"
      ],
      [
        "org"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Conflict.Attack.DetonateExplode": {
    "event_id": "LDC_KAIROS_evt_011",
    "template": "<arg1> detonated or exploded <arg4> explosive device using <arg3> to attack <arg2> target at <arg5> place",
    "i-label": 11,
    "keywords": [
      "detonate",
      "explode",
      "bombing",
      "detonation"
    ],
    "roles": [
      "Attacker",
      "Target",
      "Instrument",
      "ExplosiveDevice",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "loc",
        "gpe",
        "fac",
        "per",
        "com",
        "veh",
        "wea",
        "sid",
        "aml",
        "pla",
        "nat"
      ],
      [
        "wea",
        "com"
      ],
      [
        "wea",
        "com"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Conflict.Attack.Unspecified": {
    "event_id": "LDC_KAIROS_evt_012",
    "template": "<arg1> attacked <arg2> using <arg3> at <arg4> place",
    "i-label": 12,
    "keywords": [
      "attack",
      "war",
      "terrorism",
      "shot",
      "fire"
    ],
    "roles": [
      "Attacker",
      "Target",
      "Instrument",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid",
        "aml"
      ],
      [
        "loc",
        "gpe",
        "fac",
        "per",
        "com",
        "veh",
        "wea",
        "sid",
        "aml",
        "pla",
        "nat"
      ],
      [
        "com",
        "veh",
        "wea",
        "pth"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Conflict.Defeat.Unspecified": {
    "event_id": "LDC_KAIROS_evt_013",
    "template": "<arg1> defeated <arg2> in <arg3> conflict at <arg4> place",
    "i-label": 13,
    "keywords": [
      "defeat",
      "defeated",
      "crush",
      "victory",
      "win",
      "triumph"
    ],
    "roles": [
      "Victor",
      "Defeated",
      "ConflictOrElection",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid",
        "aml"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid",
        "aml"
      ],
      [
        "event"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Conflict.Demonstrate.DemonstrateWithViolence": {
    "event_id": "LDC_KAIROS_evt_014",
    "template": "<arg1> was in a demonstration involving violence for <arg4> topic with <arg3> visual display against <arg5> at <arg6> place, with potential involvement of <arg2> police or military",
    "i-label": 14,
    "keywords": [
      "demonstrate",
      "protest",
      "strike"
    ],
    "roles": [
      "Demonstrator",
      "Regulator",
      "VisualDisplay",
      "Topic",
      "Target",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "sid"
      ],
      [
        "per",
        "org"
      ],
      [
        "com"
      ],
      [
        "event",
        "per",
        "org",
        "gpe",
        "sid",
        "loc",
        "fac",
        "veh",
        "wea",
        "com",
        "bal",
        "mon",
        "law",
        "res",
        "val",
        "mhi",
        "inf",
        "abs",
        "aml",
        "bod",
        "nat",
        "pla",
        "pth"
      ],
      [
        "org",
        "per",
        "gpe"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Conflict.Demonstrate.Unspecified": {
    "event_id": "LDC_KAIROS_evt_015",
    "template": "<arg1> was in a demonstration for <arg4> topic with <arg3> visual display against <arg5> at <arg6> place, with potential involvement of <arg2> police or military",
    "i-label": 15,
    "keywords": [
      "demonstrate",
      "march",
      "rally"
    ],
    "roles": [
      "Demonstrator",
      "Regulator",
      "VisualDisplay",
      "Topic",
      "Target",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "sid"
      ],
      [
        "per",
        "org"
      ],
      [
        "com"
      ],
      [
        "event",
        "per",
        "org",
        "gpe",
        "sid",
        "loc",
        "fac",
        "veh",
        "wea",
        "com",
        "bal",
        "mon",
        "law",
        "res",
        "val",
        "mhi",
        "inf",
        "abs",
        "aml",
        "bod",
        "nat",
        "pla",
        "pth"
      ],
      [
        "org",
        "per",
        "gpe"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Contact.Contact.Broadcast": {
    "event_id": "LDC_KAIROS_evt_016",
    "template": "<arg1> communicated to <arg2> about <arg4> topic using <arg3> at <arg5> place (one-way communication)",
    "i-label": 16,
    "keywords": [
      "broadcast",
      "announce",
      "state"
    ],
    "roles": [
      "Communicator",
      "Recipient",
      "Instrument",
      "Topic",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "abs",
        "com"
      ],
      [
        "event",
        "per",
        "org",
        "gpe",
        "sid",
        "loc",
        "fac",
        "veh",
        "wea",
        "com",
        "bal",
        "mon",
        "law",
        "res",
        "val",
        "mhi",
        "inf",
        "abs",
        "aml",
        "bod",
        "nat",
        "pla",
        "pth"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Contact.Contact.Correspondence": {
    "event_id": "LDC_KAIROS_evt_017",
    "template": "<arg1> communicated remotely with <arg2> about <arg4> topic using <arg3> at <arg5> place",
    "i-label": 17,
    "keywords": [
      "telephone",
      "mail",
      "letter",
      "correspondence",
      "call"
    ],
    "roles": [
      "Participant",
      "Participant",
      "Instrument",
      "Topic",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "abs",
        "com"
      ],
      [
        "event",
        "per",
        "org",
        "gpe",
        "sid",
        "loc",
        "fac",
        "veh",
        "wea",
        "com",
        "bal",
        "mon",
        "law",
        "res",
        "val",
        "mhi",
        "inf",
        "abs",
        "aml",
        "bod",
        "nat",
        "pla",
        "pth"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Contact.Contact.Meet": {
    "event_id": "LDC_KAIROS_evt_018",
    "template": "<arg1> met face-to-face with <arg2> about <arg3> topic at <arg4> place",
    "i-label": 18,
    "keywords": [
      "meet",
      "meeting",
      "encounter",
      "summit"
    ],
    "roles": [
      "Participant",
      "Participant",
      "Topic",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "event",
        "per",
        "org",
        "gpe",
        "sid",
        "loc",
        "fac",
        "veh",
        "wea",
        "com",
        "bal",
        "mon",
        "law",
        "res",
        "val",
        "mhi",
        "inf",
        "abs",
        "aml",
        "bod",
        "nat",
        "pla",
        "pth"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Contact.Contact.Unspecified": {
    "event_id": "LDC_KAIROS_evt_019",
    "template": "<arg1> communicated with <arg2> about <arg3> topic at <arg4> place (document does not specify in person or not, or one-way or not)",
    "i-label": 19,
    "keywords": [
      "contact",
      "discuss",
      "talk"
    ],
    "roles": [
      "Participant",
      "Participant",
      "Topic",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "event",
        "per",
        "org",
        "gpe",
        "sid",
        "loc",
        "fac",
        "veh",
        "wea",
        "com",
        "bal",
        "mon",
        "law",
        "res",
        "val",
        "mhi",
        "inf",
        "abs",
        "aml",
        "bod",
        "nat",
        "pla",
        "pth"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Contact.Prevarication.Unspecified": {
    "event_id": "LDC_KAIROS_evt_023",
    "template": "<arg1> communicated with <arg2> about <arg3> topic at <arg4> place (document does not specify in person or not, or one-way or not)",
    "i-label": 20,
    "keywords": [
      "dodge",
      "lie",
      "prevaricate"
    ],
    "roles": [
      "Communicator",
      "Recipient",
      "Topic",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "event",
        "per",
        "org",
        "gpe",
        "sid",
        "loc",
        "fac",
        "veh",
        "wea",
        "com",
        "bal",
        "mon",
        "law",
        "res",
        "val",
        "mhi",
        "inf",
        "abs",
        "aml",
        "bod",
        "nat",
        "pla",
        "pth"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Contact.RequestCommand.Unspecified": {
    "event_id": "LDC_KAIROS_evt_027",
    "template": "<arg1> communicated with <arg2> about <arg3> topic at <arg4> place (document does not specify in person or not, or one-way or not)",
    "i-label": 21,
    "keywords": [
      "request",
      "command",
      "order"
    ],
    "roles": [
      "Communicator",
      "Recipient",
      "Topic",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "event",
        "per",
        "org",
        "gpe",
        "sid",
        "loc",
        "fac",
        "veh",
        "wea",
        "com",
        "bal",
        "mon",
        "law",
        "res",
        "val",
        "mhi",
        "inf",
        "abs",
        "aml",
        "bod",
        "nat",
        "pla",
        "pth"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Contact.ThreatenCoerce.Unspecified": {
    "event_id": "LDC_KAIROS_evt_031",
    "template": "<arg1> communicated with <arg2> about <arg3> topic at <arg4> place (document does not specify in person or not, or one-way or not)",
    "i-label": 22,
    "keywords": [
      "threaten",
      "pressurize",
      "provoke"
    ],
    "roles": [
      "Communicator",
      "Recipient",
      "Topic",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "event",
        "per",
        "org",
        "gpe",
        "sid",
        "loc",
        "fac",
        "veh",
        "wea",
        "com",
        "bal",
        "mon",
        "law",
        "res",
        "val",
        "mhi",
        "inf",
        "abs",
        "aml",
        "bod",
        "nat",
        "pla",
        "pth"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Control.ImpedeInterfereWith.Unspecified": {
    "event_id": "LDC_KAIROS_evt_032",
    "template": "<arg1> impeded or interfered with <arg2> event at <arg3> place",
    "i-label": 23,
    "keywords": [
      "impede",
      "hinder",
      "interfer",
      "disrupt"
    ],
    "roles": [
      "Impeder",
      "ImpededEvent",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "event"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Disaster.Crash.Unspecified": {
    "event_id": "LDC_KAIROS_evt_033",
    "template": "<arg1> person in <arg2> vehicle crashed into <arg3> at <arg4> place",
    "i-label": 24,
    "keywords": [
      "crash",
      "collision",
      "derailment",
      "collide",
      "accident"
    ],
    "roles": [
      "DriverPassenger",
      "Vehicle",
      "CrashObject",
      "Place"
    ],
    "role_types": [
      [
        "per"
      ],
      [
        "veh"
      ],
      [
        "aml",
        "com",
        "fac",
        "loc",
        "per",
        "veh",
        "wea"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Disaster.DiseaseOutbreak.Unspecified": {
    "event_id": "LDC_KAIROS_evt_034",
    "template": "<arg1> disease broke out among <arg2> victims or population at <arg3> place",
    "i-label": 25,
    "keywords": [
      "epidemic",
      "outbreak",
      "transmission"
    ],
    "roles": [
      "Disease",
      "Victim",
      "Place"
    ],
    "role_types": [
      [
        "mhi"
      ],
      [
        "per",
        "org",
        "sid",
        "aml",
        "pla"
      ],
      [
        "loc",
        "gpe",
        "fac",
        "veh"
      ]
    ]
  },
  "Disaster.FireExplosion.Unspecified": {
    "event_id": "LDC_KAIROS_evt_035",
    "template": "<arg1> caught fire or exploded from <arg2> instrument at <arg3> place",
    "i-label": 26,
    "keywords": [
      "fire",
      "explode",
      "blast",
      "arson",
      "burn"
    ],
    "roles": [
      "FireExplosionObject",
      "Instrument",
      "Place"
    ],
    "role_types": [
      [
        "bal",
        "veh",
        "wea",
        "fac",
        "loc",
        "com",
        "nat"
      ],
      [
        "com",
        "veh",
        "wea",
        "fac"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "GenericCrime.GenericCrime.GenericCrime": {
    "event_id": "LDC_KAIROS_evt_036",
    "template": "<arg1> committed a crime against <arg2> at <arg3> place",
    "i-label": 27,
    "keywords": [
      "crime",
      "felony",
      "offense",
      "theft",
      "murder",
      "robbery"
    ],
    "roles": [
      "Perpetrator",
      "Victim",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid",
        "aml"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Justice.Acquit.Unspecified": {
    "event_id": "LDC_KAIROS_evt_037",
    "template": "<arg1> court or judge acquitted <arg2> of <arg3> crime in <arg4> place",
    "i-label": 28,
    "keywords": [
      "acquit",
      "absolve"
    ],
    "roles": [
      "JudgeCourt",
      "Defendant",
      "Crime",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "side"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "event"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Justice.ArrestJailDetain.Unspecified": {
    "event_id": "LDC_KAIROS_evt_038",
    "template": "<arg1> arrested or jailed <arg2> for <arg3> crime at <arg4> place",
    "i-label": 29,
    "keywords": [
      "arrest",
      "jail",
      "imprison"
    ],
    "roles": [
      "Jailer",
      "Detainee",
      "Crime",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "side"
      ],
      [
        "per"
      ],
      [
        "event"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Justice.ChargeIndict.Unspecified": {
    "event_id": "LDC_KAIROS_evt_039",
    "template": "<arg1> charged or indicted <arg2> before <arg3> court or judge for <arg4> crime in <arg5> place",
    "i-label": 30,
    "keywords": [
      "charge",
      "indict",
      "accuse",
      "accusation"
    ],
    "roles": [
      "Prosecutor",
      "Defendant",
      "JudgeCourt",
      "Crime",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "event"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Justice.Convict.Unspecified": {
    "event_id": "LDC_KAIROS_evt_040",
    "template": "<arg1> court or judge convicted <arg2> of <arg3> crime in <arg4> place",
    "i-label": 31,
    "keywords": [
      "convict"
    ],
    "roles": [
      "JudgeCourt",
      "Defendant",
      "Crime",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "event"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Justice.InvestigateCrime.Unspecified": {
    "event_id": "LDC_KAIROS_evt_041",
    "template": "<arg1> investigated <arg2> for <arg3> crime in <arg4> place",
    "i-label": 32,
    "keywords": [
      "investigate",
      "investigation",
      "search",
      "suspect",
      "inquiry"
    ],
    "roles": [
      "Investigator",
      "Defendant",
      "Crime",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "event"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Justice.ReleaseParole.Unspecified": {
    "event_id": "LDC_KAIROS_evt_042",
    "template": "<arg1> court or judge released or paroled <arg2> from <arg3> crime in <arg4> place",
    "i-label": 33,
    "keywords": [
      "release",
      "parole",
      "free"
    ],
    "roles": [
      "JudgeCourt",
      "Defendant",
      "Crime",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "event"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Justice.Sentence.Unspecified": {
    "event_id": "LDC_KAIROS_evt_043",
    "template": "<arg1> court or judge sentenced <arg2> for <arg3> crime to <arg4> sentence in <arg5> place",
    "i-label": 34,
    "keywords": [
      "sentence"
    ],
    "roles": [
      "JudgeCourt",
      "Defendant",
      "Crime",
      "Sentence",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "event"
      ],
      [
        "sen"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Justice.TrialHearing.Unspecified": {
    "event_id": "LDC_KAIROS_evt_044",
    "template": "<arg1> tried <arg2> before <arg3> court or judge for <arg4> crime in <arg5> place",
    "i-label": 35,
    "keywords": [
      "trial",
      "tried",
      "hearing",
      "testify"
    ],
    "roles": [
      "Prosecutor",
      "Defendant",
      "JudgeCourt",
      "Crime",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "event"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Life.Consume.Unspecified": {
    "event_id": "LDC_KAIROS_evt_045",
    "template": "<arg1> consumed <arg2> at <arg3> place",
    "i-label": 36,
    "keywords": [
      "consume",
      "eat",
      "drink",
      "ingest"
    ],
    "roles": [
      "ConsumingEntity",
      "ConsumedThing",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "aml"
      ],
      [
        "com"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Life.Die.Unspecified": {
    "event_id": "LDC_KAIROS_evt_046",
    "template": "<arg1> died at <arg2> place from <arg4> medical issue, killed by <arg3> killer",
    "i-label": 37,
    "keywords": [
      "die",
      "kill",
      "death",
      "assasinate",
      "suicide"
    ],
    "roles": [
      "Victim",
      "Place",
      "Killer",
      "MedicalIssue"
    ],
    "role_types": [
      [
        "per",
        "aml"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid",
        "aml"
      ],
      [
        "mhi"
      ]
    ]
  },
  "Life.Illness.Unspecified": {
    "event_id": "LDC_KAIROS_evt_047",
    "template": "<arg1> has <arg3> sickness or illness at <arg4> place, deliberately infected by <arg2>",
    "i-label": 38,
    "keywords": [
      "illness",
      "disease",
      "sickness"
    ],
    "roles": [
      "Victim",
      "DeliberateInjurer",
      "Disease",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "aml"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "mhi"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Life.Infect.Unspecified": {
    "event_id": "LDC_KAIROS_evt_048",
    "template": "<arg1> was infected with <arg2> from <arg3> at <arg4> place",
    "i-label": 39,
    "keywords": [
      "infect",
      "spread",
      "contaminate"
    ],
    "roles": [
      "Victim",
      "InfectingAgent",
      "Source",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "aml"
      ],
      [
        "pth"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid",
        "loc",
        "fac",
        "veh",
        "wea",
        "com",
        "bal",
        "mon",
        "mhi",
        "aml",
        "bod",
        "nat",
        "pla",
        "pth"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Life.Injure.Unspecified": {
    "event_id": "LDC_KAIROS_evt_049",
    "template": "<arg1> was injured by <arg2> using <arg3> in <arg4> body part with <arg5> medical issue at <arg6> place",
    "i-label": 40,
    "keywords": [
      "injure",
      "hurt",
      "wound"
    ],
    "roles": [
      "Victim",
      "Injurer",
      "Instrument",
      "BodyPart",
      "MedicalCondition",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "aml"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid",
        "aml"
      ],
      [
        "bal",
        "com",
        "veh",
        "wea",
        "fac",
        "mon"
      ],
      [
        "bod"
      ],
      [
        "mhi"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Medical.Diagnosis.Unspecified": {
    "event_id": "LDC_KAIROS_evt_050",
    "template": "<arg1> treater diagnosed <arg2> patient with <arg3> symptom for <arg4> medical issue at <arg5> place",
    "i-label": 41,
    "keywords": [
      "diagnosis",
      "identification"
    ],
    "roles": [
      "Treater",
      "Patient",
      "SymptomSign",
      "MedicalCondition",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "per",
        "aml"
      ],
      [
        "mhi"
      ],
      [
        "mhi"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Medical.Intervention.Unspecified": {
    "event_id": "LDC_KAIROS_evt_051",
    "template": "<arg1> treater treated <arg2> patient for <arg3> medical issue with <arg4> means at <arg5> place",
    "i-label": 42,
    "keywords": [
      "treat",
      "surgery",
      "hospitalize",
      "medicate",
      "medicine",
      "rehabilitation"
    ],
    "roles": [
      "Treater",
      "Patient",
      "MedicalIssue",
      "Instrument",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "per",
        "aml"
      ],
      [
        "mhi"
      ],
      [
        "com"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Medical.Vaccinate.Unspecified": {
    "event_id": "LDC_KAIROS_evt_052",
    "template": "<arg1> treater vaccinated <arg2> patient via <arg4> vaccination method for <arg3> medical issue at <arg5> place",
    "i-label": 43,
    "keywords": [
      "vaccinate"
    ],
    "roles": [
      "Treater",
      "Patient",
      "VaccineTarget",
      "VaccineMethod",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "per",
        "aml"
      ],
      [
        "mhi"
      ],
      [
        "com"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Movement.Transportation.Evacuation": {
    "event_id": "LDC_KAIROS_evt_053",
    "template": "<arg1> transported <arg2> in <arg3> from <arg4> place to <arg5> place",
    "i-label": 44,
    "keywords": [
      "evacuate",
      "evacuation",
      "retreat",
      "escape"
    ],
    "roles": [
      "Transporter",
      "PassengerArtifact",
      "Vehicle",
      "Origin",
      "Destination"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "per",
        "aml"
      ],
      [
        "veh"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Movement.Transportation.IllegalTransportation": {
    "event_id": "LDC_KAIROS_evt_055",
    "template": "<arg1> illegally transported <arg2> in <arg3> from <arg4> place to <arg5> place",
    "i-label": 45,
    "keywords": [
      "smuggle",
      "trespass",
      "intrude"
    ],
    "roles": [
      "Transporter",
      "PassengerArtifact",
      "Vehicle",
      "Origin",
      "Destination"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "per",
        "bal",
        "com",
        "fac",
        "loc",
        "mon",
        "veh",
        "wea",
        "aml",
        "pth",
        "pla",
        "bod",
        "nat"
      ],
      [
        "veh"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Movement.Transportation.PreventPassage": {
    "event_id": "LDC_KAIROS_evt_056",
    "template": "<arg4> prevents <arg1> from entering <arg6> place from <arg5> place to transport <arg2> using <arg3> vehicle",
    "i-label": 46,
    "keywords": [
      "block",
      "stop",
      "obstruct"
    ],
    "roles": [
      "Transporter",
      "PassengerArtifact",
      "Vehicle",
      "Preventer",
      "Origin",
      "Destination"
    ],
    "role_types": [
      [
        "per",
        "org",
        "sid",
        "gpe"
      ],
      [
        "per",
        "bal",
        "com",
        "fac",
        "loc",
        "mon",
        "veh",
        "wea",
        "aml",
        "pth",
        "pla",
        "bod",
        "nat"
      ],
      [
        "veh"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Movement.Transportation.Unspecified": {
    "event_id": "LDC_KAIROS_evt_057",
    "template": "<arg1> transported <arg2> in <arg3> from <arg4> place to <arg5> place",
    "i-label": 47,
    "keywords": [
      "transport",
      "move",
      "travel",
      "head"
    ],
    "roles": [
      "Transporter",
      "PassengerArtifact",
      "Vehicle",
      "Origin",
      "Destination"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "per",
        "bal",
        "com",
        "fac",
        "loc",
        "mon",
        "veh",
        "wea",
        "aml",
        "pth",
        "pla",
        "bod",
        "nat"
      ],
      [
        "veh"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Personnel.EndPosition.Unspecified": {
    "event_id": "LDC_KAIROS_evt_063",
    "template": "<arg1> stopped working in <arg3> position at <arg2> organization in <arg4> place",
    "i-label": 48,
    "keywords": [
      "resign",
      "retire",
      "former",
      "fire",
      "dismiss"
    ],
    "roles": [
      "Employee",
      "PlaceOfEmployment",
      "Position",
      "Place"
    ],
    "role_types": [
      [
        "per"
      ],
      [
        "gpe",
        "org"
      ],
      [
        "ttl"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Personnel.StartPosition.Unspecified": {
    "event_id": "LDC_KAIROS_evt_064",
    "template": "<arg1> started working in <arg3> position at <arg2> organization in <arg4> place",
    "i-label": 49,
    "keywords": [
      "hire",
      "employ",
      "appoint"
    ],
    "roles": [
      "Employee",
      "PlaceOfEmployment",
      "Position",
      "Place"
    ],
    "role_types": [
      [
        "per"
      ],
      [
        "gpe",
        "org"
      ],
      [
        "ttl"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Transaction.Donation.Unspecified": {
    "event_id": "LDC_KAIROS_evt_066",
    "template": "<arg1> gave <arg4> to <arg2> for the benefit of <arg3> at <arg5> place",
    "i-label": 50,
    "keywords": [
      "donate",
      "aid",
      "donation",
      "charity",
      "relief"
    ],
    "roles": [
      "Giver",
      "Recipient",
      "Beneficiary",
      "ArtifactMoney",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "mon",
        "com",
        "bal",
        "fac",
        "veh",
        "wea",
        "aml",
        "pla",
        "nat",
        "abs",
        "bod"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  },
  "Transaction.ExchangeBuySell.Unspecified": {
    "event_id": "LDC_KAIROS_evt_067",
    "template": "<arg1> bought, sold, or traded <arg3> to <arg2> in exchange for <arg4> for the benefit of <arg5> at <arg6> place",
    "i-label": 51,
    "keywords": [
      "buy",
      "sell",
      "purchase",
      "rent",
      "trade"
    ],
    "roles": [
      "Giver",
      "Recipient",
      "AcquiredEntity",
      "PaymentBarter",
      "Beneficiary",
      "Place"
    ],
    "role_types": [
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "bal",
        "com",
        "gpe",
        "fac",
        "loc",
        "mon",
        "org",
        "veh",
        "wea",
        "abs",
        "aml",
        "nat",
        "pla",
        "pth"
      ],
      [
        "bal",
        "com",
        "gpe",
        "fac",
        "loc",
        "mon",
        "org",
        "veh",
        "wea",
        "abs",
        "aml",
        "nat",
        "pla",
        "pth"
      ],
      [
        "per",
        "org",
        "gpe",
        "sid"
      ],
      [
        "loc",
        "gpe",
        "fac"
      ]
    ]
  }
}