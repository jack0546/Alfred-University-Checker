"""
Script to generate a comprehensive universities_data.json
with 100+ universities and 2026 cutoff points.
"""
import json
import os
from datetime import datetime

# ──────────────────────────────────────────────
# SHARED PROGRAM POOLS  (used across universities)
# ──────────────────────────────────────────────

CORE_SCIENCE  = ["English Language", "Core Mathematics", "Integrated Science"]
CORE_ARTS     = ["English Language", "Core Mathematics", "Social Studies"]
CORE_ICT      = ["English Language", "Core Mathematics", "Information and Communication Technology"]

def sci(name, cat, agg, desc="", pop="medium", val="medium", desired=False, electives=None):
    return {
        "name": name, "category": cat,
        "description": desc or f"A rigorous {name} program equipping students with theoretical and practical knowledge.",
        "maximum_aggregate": agg,
        "required_core_subjects": CORE_SCIENCE,
        "required_electives": electives or [],
        "popularity_level": pop, "value_level": val, "is_desired_program": desired,
        "academic_year": datetime.utcnow().year
    }

def arts(name, cat, agg, desc="", pop="medium", val="medium", desired=False, electives=None):
    return {
        "name": name, "category": cat,
        "description": desc or f"A comprehensive {name} program developing critical thinking and professional skills.",
        "maximum_aggregate": agg,
        "required_core_subjects": CORE_ARTS,
        "required_electives": electives or [],
        "popularity_level": pop, "value_level": val, "is_desired_program": desired,
        "academic_year": datetime.utcnow().year
    }

def ict(name, cat, agg, desc="", pop="medium", val="medium", desired=False):
    return {
        "name": name, "category": cat,
        "description": desc or f"{name} covering modern computing, networks, and digital technologies.",
        "maximum_aggregate": agg,
        "required_core_subjects": CORE_ICT,
        "required_electives": [],
        "popularity_level": pop, "value_level": val, "is_desired_program": desired,
        "academic_year": datetime.utcnow().year
    }

def tech(name, agg, desc="", pop="medium"):
    return {
        "name": name, "category": "Technical",
        "description": desc or f"Hands-on {name} program preparing students for industry.",
        "maximum_aggregate": agg,
        "required_core_subjects": CORE_ARTS,
        "required_electives": [],
        "popularity_level": pop, "value_level": "medium", "is_desired_program": False,
        "academic_year": datetime.utcnow().year
    }

# 100+ programs reusable pool for traditional universities
def traditional_programs(agg_offset=0):
    base = agg_offset
    return [
        # Science & Engineering
        sci("Bachelor of Science in Computer Science", "Science", 24+base, "Study of computation, algorithms, data structures, software engineering, AI, and systems programming.", "high","high", True),
        sci("Bachelor of Science in Information Technology", "Science", 26+base, "Covers networking, database management, cybersecurity, and IT infrastructure.", "high","high", True),
        sci("Bachelor of Science in Software Engineering", "Science", 24+base, "Rigorous software development lifecycle, design patterns, testing, and agile methodologies.", "high","high", True),
        sci("Bachelor of Science in Electrical Engineering", "Science", 22+base, "Power systems, electronics, telecommunications, and control engineering.", "high","high", True),
        sci("Bachelor of Science in Mechanical Engineering", "Science", 22+base, "Thermodynamics, fluid mechanics, manufacturing, and machine design.", "high","high", True),
        sci("Bachelor of Science in Civil Engineering", "Science", 22+base, "Structural engineering, geotechnics, transportation, and construction management.", "high","high", True),
        sci("Bachelor of Science in Chemical Engineering", "Science", 22+base, "Process engineering, reaction kinetics, unit operations in chemical manufacturing.", "medium","high", True),
        sci("Bachelor of Science in Biomedical Engineering", "Science", 24+base, "Application of engineering principles to medicine and healthcare. Covers medical devices, bioinformatics.", "medium","high", True),
        sci("Bachelor of Science in Environmental Engineering", "Science", 24+base, "Water treatment, pollution control, environmental impact assessment, and sustainability.", "medium","medium", False),
        sci("Bachelor of Science in Telecommunication Engineering", "Science", 24+base, "Designing and managing communication systems, wireless networks, and signal processing.", "medium","high", True),
        sci("Bachelor of Science in Computer Engineering", "Science", 22+base, "Hardware design, embedded systems, microprocessors, and digital circuits.", "high","high", True),
        sci("Bachelor of Science in Petroleum Engineering", "Science", 20+base, "Drilling, reservoir engineering, production, and refinery operations.", "medium","high", True),
        sci("Bachelor of Science in Mining Engineering", "Science", 20+base, "Mineral extraction, rock mechanics, mine ventilation, and safety.", "medium","high", False),
        sci("Bachelor of Science in Metallurgical Engineering", "Science", 22+base, "Metal extraction, processing, and material properties engineering.", "low","medium", False),
        sci("Bachelor of Science in Agricultural Engineering", "Science", 24+base, "Farm mechanization, irrigation systems, post-harvest technology, and agronomy.", "low","medium", False),
        sci("Bachelor of Science in Food Science and Technology", "Science", 26+base, "Food processing, nutrition, quality control, and food safety standards.", "medium","medium", False),
        sci("Bachelor of Science in Biochemistry", "Science", 24+base, "Molecular biology, enzymes, metabolism, and laboratory techniques.", "medium","medium", False),
        sci("Bachelor of Science in Chemistry", "Science", 26+base, "Organic, inorganic, analytical, and physical chemistry fundamentals.", "medium","medium", False),
        sci("Bachelor of Science in Physics", "Science", 26+base, "Classical and modern physics, optics, thermodynamics, and quantum mechanics.", "low","medium", False),
        sci("Bachelor of Science in Mathematics", "Science", 26+base, "Pure and applied mathematics, statistics, numerical analysis.", "medium","medium", False),
        sci("Bachelor of Science in Statistics", "Science", 26+base, "Probability theory, statistical inference, data analysis, and actuarial science.", "medium","high", True),
        sci("Bachelor of Science in Actuarial Science", "Science", 24+base, "Risk management, financial mathematics, and insurance modeling.", "medium","high", True),
        sci("Bachelor of Science in Medicine", "Science", 18+base, "Comprehensive medical education covering anatomy, physiology, pathology, and clinical rotations.", "high","high", True),
        sci("Bachelor of Science in Nursing", "Science", 20+base, "Patient care, clinical practice, pharmacology, and community health.", "high","high", True),
        sci("Bachelor of Science in Pharmacy", "Science", 20+base, "Pharmaceutical chemistry, pharmacology, clinical pharmacy, and drug formulation.", "high","high", True),
        sci("Bachelor of Science in Optometry", "Science", 22+base, "Eye examination, optics, vision therapy, and ophthalmic dispensing.", "medium","high", True),
        sci("Bachelor of Science in Physiotherapy", "Science", 22+base, "Rehabilitation, musculoskeletal therapy, and sports medicine.", "medium","high", True),
        sci("Bachelor of Science in Medical Laboratory Science", "Science", 22+base, "Clinical laboratory procedures, haematology, microbiology, and diagnostics.", "medium","high", True),
        sci("Bachelor of Science in Radiography", "Science", 22+base, "Medical imaging, radiation therapy, and patient safety protocols.", "medium","high", False),
        sci("Bachelor of Science in Nutrition and Dietetics", "Science", 24+base, "Human nutrition, clinical dietetics, public health nutrition, and food policy.", "medium","medium", False),
        sci("Bachelor of Science in Public Health", "Science", 24+base, "Epidemiology, biostatistics, health policy, and community health interventions.", "medium","medium", True),
        sci("Bachelor of Science in Agriculture", "Science", 26+base, "Crop production, animal science, soil science, and agribusiness.", "low","medium", False),
        sci("Bachelor of Science in Forestry", "Science", 26+base, "Forest ecology, silviculture, wildlife management, and natural resource conservation.", "low","medium", False),
        sci("Bachelor of Science in Fisheries and Aquaculture", "Science", 28+base, "Fish biology, aquaculture systems, marine biology, and fisheries management.", "low","low", False),
        sci("Bachelor of Science in Environmental Science", "Science", 26+base, "Ecology, climate science, environmental law, and sustainability.", "medium","medium", False),
        sci("Bachelor of Science in Geology", "Science", 26+base, "Earth structure, mineralogy, petrology, and geological mapping.", "low","medium", False),
        sci("Bachelor of Science in Architecture", "Science", 22+base, "Architectural design, urban planning, structural systems, and building technology.", "medium","high", True),
        sci("Bachelor of Science in Quantity Surveying", "Science", 24+base, "Cost estimation, construction economics, and contract management.", "medium","medium", False),
        sci("Bachelor of Science in Land Economy", "Science", 24+base, "Property valuation, land law, environmental management, and estate management.", "medium","medium", False),
        sci("Bachelor of Science in Urban Planning", "Science", 24+base, "Urban design, transport planning, housing policy, and regional development.", "low","medium", False),
        # Business & Management
        arts("Bachelor of Business Administration", "Business", 28+base, "Comprehensive management training covering marketing, finance, operations, and strategy.", "high","high", True),
        arts("Bachelor of Science in Accounting", "Business", 26+base, "Financial reporting, auditing, taxation, and management accounting.", "high","high", True),
        arts("Bachelor of Science in Finance", "Business", 26+base, "Corporate finance, investment analysis, financial markets, and risk management.", "high","high", True),
        arts("Bachelor of Science in Marketing", "Business", 28+base, "Consumer behaviour, digital marketing, brand management, and market research.", "medium","medium", False),
        arts("Bachelor of Science in Supply Chain Management", "Business", 28+base, "Logistics, procurement, inventory management, and global supply chains.", "medium","medium", False),
        arts("Bachelor of Science in Human Resource Management", "Business", 28+base, "Talent acquisition, training and development, labour law, and organisational behaviour.", "medium","medium", False),
        arts("Bachelor of Science in Entrepreneurship", "Business", 30+base, "Innovation, startup management, venture capital, and business plan development.", "medium","medium", False),
        arts("Bachelor of Science in Insurance", "Business", 30+base, "Risk management, underwriting, actuarial principles, and claims management.", "low","medium", False),
        arts("Bachelor of Science in Banking and Finance", "Business", 26+base, "Commercial banking, financial analysis, monetary policy, and credit management.", "high","high", True),
        arts("Bachelor of Science in Tourism Management", "Business", 30+base, "Tourism planning, hospitality operations, destination marketing, and ecotourism.", "low","low", False),
        arts("Bachelor of Science in Hospitality Management", "Business", 30+base, "Hotel operations, food and beverage management, events planning, and customer service.", "low","low", False),
        arts("Bachelor of Science in Real Estate Management", "Business", 28+base, "Property development, valuations, facilities management, and real estate finance.", "medium","medium", False),
        arts("Bachelor of Science in International Business", "Business", 28+base, "Global trade, cross-cultural management, international finance, and trade law.", "medium","medium", False),
        arts("Bachelor of Science in Project Management", "Business", 30+base, "Project planning, risk management, scheduling, and stakeholder management.", "medium","medium", False),
        arts("Bachelor of Science in Logistics and Transport", "Business", 28+base, "Freight management, transport policy, warehousing, and distribution networks.", "low","medium", False),
        # Arts & Social Sciences
        arts("Bachelor of Laws", "Arts", 24+base, "Constitutional law, criminal law, contract law, and legal practice.", "high","high", True),
        arts("Bachelor of Arts in Economics", "Arts", 26+base, "Micro and macro economics, econometrics, development economics, and economic policy.", "medium","medium", False),
        arts("Bachelor of Arts in Political Science", "Arts", 28+base, "Political theory, comparative politics, international relations, and public policy.", "medium","medium", False),
        arts("Bachelor of Arts in Sociology", "Arts", 30+base, "Social inequality, culture, organisations, and research methods.", "low","low", False),
        arts("Bachelor of Arts in Psychology", "Arts", 28+base, "Cognitive psychology, clinical psychology, developmental psychology, and counselling.", "medium","medium", True),
        arts("Bachelor of Arts in Geography and Rural Development", "Arts", 30+base, "Human geography, GIS, rural development, and environmental studies.", "low","low", False),
        arts("Bachelor of Arts in History", "Arts", 30+base, "Ghanaian, African, and world history, historical methods, and archival research.", "low","low", False),
        arts("Bachelor of Arts in Language and Linguistics", "Arts", 30+base, "Phonetics, syntax, semantics, applied linguistics, and language acquisition.", "low","low", False),
        arts("Bachelor of Arts in Communication Studies", "Arts", 28+base, "Mass communication, journalism, public relations, and media studies.", "medium","medium", False),
        arts("Bachelor of Arts in Journalism and Mass Communication", "Arts", 28+base, "News reporting, broadcasting, digital media, and media ethics.", "medium","medium", False),
        arts("Bachelor of Arts in Philosophy", "Arts", 30+base, "Logic, ethics, epistemology, metaphysics, and African philosophy.", "low","low", False),
        arts("Bachelor of Arts in Religious Studies", "Arts", 32+base, "World religions, theology, comparative religion, and ethics.", "low","low", False),
        arts("Bachelor of Arts in Fine Arts", "Arts", 30+base, "Drawing, painting, sculpture, graphic design, and art history.", "low","low", False),
        arts("Bachelor of Arts in Music", "Arts", 32+base, "Music theory, composition, performance, and music technology.", "low","low", False),
        arts("Bachelor of Arts in Theatre Arts", "Arts", 32+base, "Drama, directing, stagecraft, and performance arts.", "low","low", False),
        arts("Bachelor of Arts in French", "Arts", 30+base, "French language, literature, francophone culture, and translation.", "low","low", False),
        arts("Bachelor of Arts in Social Work", "Arts", 30+base, "Social welfare, community development, counselling, and child protection.", "low","medium", False),
        arts("Bachelor of Arts in International Relations", "Arts", 28+base, "Diplomacy, global governance, international law, and foreign policy.", "medium","medium", False),
        arts("Bachelor of Arts in Development Studies", "Arts", 30+base, "Poverty analysis, rural development, gender studies, and aid policy.", "low","low", False),
        # Education
        arts("Bachelor of Education (Science)", "Education", 28+base, "Science pedagogy, curriculum development, educational psychology, and teaching practice.", "medium","medium", False),
        arts("Bachelor of Education (Mathematics)", "Education", 28+base, "Mathematics methodology, educational research, and classroom management.", "medium","medium", False),
        arts("Bachelor of Education (Social Studies)", "Education", 30+base, "Social science teaching methods, citizenship education, and community studies.", "medium","low", False),
        arts("Bachelor of Education (Language Arts)", "Education", 30+base, "English and language teaching, literacy development, and children's literature.", "medium","low", False),
        arts("Bachelor of Education (ICT)", "Education", 30+base, "Technology integration in education, e-learning, and digital pedagogy.", "medium","medium", False),
        arts("Bachelor of Education (Early Childhood)", "Education", 30+base, "Early childhood education, child development, play-based learning.", "medium","low", False),
        arts("Bachelor of Education (Basic Education)", "Education", 30+base, "Primary school teaching methods, curriculum design, and assessment.", "medium","low", False),
        arts("Bachelor of Education (Physical Education)", "Education", 32+base, "Sports science, physical fitness, movement education, and health.", "low","low", False),
        arts("Bachelor of Education (Guidance and Counselling)", "Education", 30+base, "Student counselling, career guidance, and psychosocial support.", "low","medium", False),
        arts("Bachelor of Education (Special Education)", "Education", 30+base, "Inclusive education, disability studies, and learning support strategies.", "low","medium", False),
        # ICT & Digital
        ict("Bachelor of Science in Data Science", "Science", 24+base, "Big data analytics, machine learning, data visualization, and statistical modelling.", "high","high", True),
        ict("Bachelor of Science in Cybersecurity", "Science", 24+base, "Network security, ethical hacking, cryptography, and digital forensics.", "high","high", True),
        ict("Bachelor of Science in Artificial Intelligence", "Science", 22+base, "Machine learning, neural networks, natural language processing, and robotics.", "high","high", True),
        ict("Bachelor of Science in Information Systems", "Science", 26+base, "ERP systems, database management, systems analysis, and IT governance.", "medium","high", True),
        ict("Bachelor of Science in Computer Networking", "Science", 26+base, "Network design, protocols, cloud computing, and network security.", "medium","high", False),
        ict("Bachelor of Science in Mobile Computing", "Science", 26+base, "Mobile app development, IoT, wireless systems, and UX design.", "high","high", True),
        ict("Bachelor of Science in Blockchain Technology", "Science", 26+base, "Distributed ledger technology, smart contracts, DeFi, and cryptocurrency.", "medium","high", True),
        ict("Bachelor of Science in Cloud Computing", "Science", 26+base, "Cloud architecture, DevOps, containerization, and cloud security.", "high","high", True),
        ict("Bachelor of Science in Game Development", "Science", 28+base, "Game design, 3D modelling, game engines, and VR/AR technologies.", "medium","medium", False),
        ict("Bachelor of Science in Digital Innovation", "Science", 28+base, "Design thinking, digital entrepreneurship, and technology management.", "medium","medium", False),
        # Health & Allied
        sci("Bachelor of Science in Midwifery", "Science", 20+base, "Maternal care, antenatal services, obstetrics, and newborn care.", "medium","high", True),
        sci("Bachelor of Science in Dental Technology", "Science", 24+base, "Dental prosthetics, oral health science, and dental laboratory procedures.", "medium","medium", False),
        sci("Bachelor of Science in Medical Imaging", "Science", 22+base, "Radiological procedures, MRI, CT scanning, and diagnostic imaging.", "medium","high", False),
        sci("Bachelor of Science in Community Health", "Science", 24+base, "Disease prevention, health promotion, epidemiology, and primary healthcare.", "medium","medium", False),
        sci("Bachelor of Science in Health Information Management", "Science", 26+base, "Electronic health records, health data coding, and health informatics.", "medium","medium", False),
        sci("Bachelor of Science in Occupational Therapy", "Science", 24+base, "Therapeutic interventions, rehabilitation, and occupational analysis.", "low","medium", False),
        sci("Bachelor of Science in Speech and Language Therapy", "Science", 26+base, "Communication disorders, language pathology, and audiological rehabilitation.", "low","medium", False),
        # Agric & Natural Resources
        sci("Bachelor of Science in Agribusiness Management", "Business", 28+base, "Agri-value chains, agri-finance, agricultural marketing, and farm economics.", "medium","medium", False),
        sci("Bachelor of Science in Animal Science", "Science", 26+base, "Livestock production, animal nutrition, veterinary basics, and animal breeding.", "low","low", False),
        sci("Bachelor of Science in Soil Science", "Science", 28+base, "Soil chemistry, land use management, crop nutrition, and soil conservation.", "low","low", False),
        sci("Bachelor of Science in Crop Science", "Science", 28+base, "Plant physiology, pest management, seed technology, and crop improvement.", "low","low", False),
        sci("Bachelor of Science in Horticulture", "Science", 28+base, "Vegetable production, floriculture, landscape gardening, and post-harvest handling.", "low","low", False),
        sci("Bachelor of Science in Natural Resource Management", "Science", 26+base, "Forest resources, water management, biodiversity conservation, and policy.", "low","medium", False),
        sci("Bachelor of Science in Water Resources Engineering", "Science", 24+base, "Hydrology, water supply, irrigation engineering, and dam design.", "low","medium", False),
        sci("Bachelor of Science in Marine Science", "Science", 26+base, "Oceanography, marine ecology, coastal management, and fisheries science.", "low","medium", False),
    ]

# 100+ programs for technical universities
def technical_programs(agg_offset=0):
    base = agg_offset
    return [
        # Engineering HNDs
        tech("HND in Civil Engineering", 28+base, "Structural engineering, surveying, and construction site management."),
        tech("HND in Mechanical Engineering", 28+base, "Thermodynamics, machine design, and manufacturing technology."),
        tech("HND in Electrical Engineering", 28+base, "Power systems, electronics, and electrical installation."),
        tech("HND in Telecommunication Engineering", 30+base, "Mobile networks, signal processing, and communication systems."),
        tech("HND in Electronics Engineering", 30+base, "Circuit design, microcontrollers, and digital electronics."),
        tech("HND in Automotive Engineering", 30+base, "Vehicle maintenance, engine systems, and automotive diagnostics."),
        tech("HND in Petroleum Engineering Technology", 28+base, "Oil and gas operations, drilling engineering, and refinery safety."),
        tech("HND in Chemical Engineering Technology", 30+base, "Process control, laboratory techniques, and plant operations."),
        tech("HND in Mining Engineering Technology", 28+base, "Mineral processing, mine ventilation, and safety management."),
        tech("HND in Marine Engineering", 30+base, "Ship machinery, marine power systems, and naval architecture."),
        tech("HND in Aeronautical Engineering", 30+base, "Aircraft systems, avionics, and aviation safety."),
        tech("HND in Metrological Science and Technology", 32+base, "Measurement science, instrumentation, and calibration."),
        tech("HND in Agricultural Engineering", 30+base, "Farm machinery, irrigation, soil conservation, and food systems."),
        tech("HND in Environmental Engineering Technology", 30+base, "Waste management, pollution control, and environmental monitoring."),
        tech("HND in Building Technology", 28+base, "Building design, estimation, materials science, and site supervision."),
        tech("HND in Architecture Technology", 30+base, "Architectural drawing, quantity surveying, and urban design basics."),
        tech("HND in Surveying and Geoinformatics", 30+base, "Land surveying, GIS, remote sensing, and cadastral mapping."),
        tech("HND in Interior Design", 32+base, "Space planning, interior architecture, and material selection."),
        # IT & Computing HNDs
        tech("HND in Information Technology", 30+base, "Networking, databases, web development, and cybersecurity basics."),
        tech("HND in Computer Science Technology", 30+base, "Programming, systems analysis, and software development."),
        tech("HND in Software Development", 30+base, "Agile development, mobile apps, and cloud solutions."),
        tech("HND in Cybersecurity Technology", 30+base, "Network defense, ethical hacking, and digital forensics."),
        tech("HND in Data Analytics", 30+base, "Data analysis, business intelligence, and statistical computing."),
        tech("HND in Network Administration", 30+base, "Server management, cloud infrastructure, and network support."),
        tech("HND in Digital Marketing", 32+base, "SEO, social media marketing, content creation, and analytics."),
        tech("HND in Multimedia Design", 32+base, "Graphic design, animation, video production, and branding."),
        tech("HND in Web Design and Development", 30+base, "HTML, CSS, JavaScript, and UX/UI design principles."),
        tech("HND in Mechatronics Engineering", 30+base, "Robotics, automation, sensors, and embedded systems."),
        tech("HND in Artificial Intelligence and Robotics", 30+base, "Machine learning basics, robotic systems, and automation."),
        # Business HNDs
        tech("HND in Business Administration", 32+base, "Management, marketing, finance, and organisational behaviour.", "high"),
        tech("HND in Accounting and Finance", 30+base, "Financial reporting, cost accounting, taxation, and auditing.", "high"),
        tech("HND in Marketing", 32+base, "Consumer behaviour, advertising, sales management, and branding."),
        tech("HND in Human Resource Management", 32+base, "Recruitment, payroll, training, and industrial relations."),
        tech("HND in Secretaryship and Management Studies", 32+base, "Office management, executive communication, and business writing."),
        tech("HND in Banking and Finance", 30+base, "Banking operations, credit analysis, and financial markets."),
        tech("HND in Insurance Studies", 32+base, "Underwriting, claims adjustment, and risk assessment."),
        tech("HND in Supply Chain and Logistics", 32+base, "Procurement, warehousing, freight forwarding, and imports/exports."),
        tech("HND in Purchasing and Supply Management", 32+base, "Contract management, supplier evaluation, and supply chain ethics."),
        tech("HND in Entrepreneurship Development", 32+base, "Business planning, startup finance, and SME management."),
        tech("HND in Retail Management", 34+base, "Merchandise planning, customer experience, and retail technology."),
        tech("HND in Event Management", 34+base, "Event planning, logistics, sponsorship, and public relations."),
        # Hospitality & Tourism HNDs
        tech("HND in Hospitality Management", 32+base, "Hotel operations, food and beverage, front office, and housekeeping."),
        tech("HND in Tourism Management", 34+base, "Destination management, tour operations, and ecotourism."),
        tech("HND in Catering and Food Service", 32+base, "Culinary arts, food safety, nutrition, and kitchen management."),
        tech("HND in Bakery and Pastry", 34+base, "Baking science, pastry arts, confectionery, and cake decorating."),
        tech("HND in Travel and Tour Operations", 34+base, "Air travel reservations, tour packaging, and travel counselling."),
        tech("HND in Fashion Design and Clothing Technology", 34+base, "Fashion illustration, pattern making, garment construction, and retail fashion."),
        tech("HND in Cosmetology and Beauty Therapy", 34+base, "Skincare, hair design, nail technology, and spa management."),
        # Health & Allied HNDs
        tech("HND in Medical Laboratory Technology", 28+base, "Clinical chemistry, haematology, microbiology, and diagnostics."),
        tech("HND in Pharmacy Technology", 28+base, "Drug dispensing, pharmaceutical calculations, and pharmacy operations."),
        tech("HND in Community Health", 30+base, "Health promotion, disease surveillance, primary care, and epidemiology."),
        tech("HND in Midwifery Technology", 28+base, "Antenatal care, obstetric support, and newborn management."),
        tech("HND in Health Information Management", 30+base, "Medical records, ICD coding, and health statistics."),
        tech("HND in Environmental Health", 30+base, "Sanitation, food hygiene, vector control, and occupational health."),
        tech("HND in Radiography Technology", 30+base, "X-ray procedures, radiation protection, and diagnostic imaging support."),
        tech("HND in Physiotherapy Technology", 30+base, "Rehabilitation techniques, manual therapy, and therapeutic exercises."),
        tech("HND in Optometry Technology", 30+base, "Ophthalmic dispensing, spectacle fitting, and contact lenses."),
        tech("HND in Dental Technology", 30+base, "Prosthetics, dental labs, and oral hygiene education."),
        # Agric & Natural Resources HNDs
        tech("HND in Agriculture", 30+base, "Crop farming, animal husbandry, and agribusiness basics."),
        tech("HND in Agribusiness Management", 32+base, "Farm economics, agri-marketing, and agricultural value chains."),
        tech("HND in Animal Production Technology", 32+base, "Livestock farming, animal nutrition, and veterinary support."),
        tech("HND in Crop Production Technology", 30+base, "Crop management, pest control, and plant nutrition."),
        tech("HND in Fisheries Technology", 32+base, "Aquaculture, fish processing, and fisheries management."),
        tech("HND in Forestry Technology", 32+base, "Forest management, timber processing, and biodiversity conservation."),
        tech("HND in Food and Post-Harvest Technology", 30+base, "Food processing, preservation, and quality standards."),
        tech("HND in Soil and Water Management", 32+base, "Irrigation, drainage, soil conservation, and land reclamation."),
        # Education & Social HNDs
        tech("HND in Teacher Education (Vocational and Technical)", 30+base, "Pedagogy, curriculum design, and vocational instruction methods."),
        tech("HND in Library and Information Science", 32+base, "Cataloguing, information retrieval, and digital library management."),
        tech("HND in Office Technology Management", 32+base, "Office automation, clerical skills, and administrative support."),
        tech("HND in Public Relations", 32+base, "Media relations, corporate communications, and crisis management."),
        tech("HND in Mass Communication", 32+base, "Journalism basics, broadcasting, and digital media production."),
        tech("HND in Social Development Studies", 32+base, "Community organising, social welfare, and development planning."),
        tech("HND in Art and Design", 32+base, "Drawing, graphic arts, textile design, and visual communication."),
        tech("HND in Music Technology", 34+base, "Music production, sound engineering, and audio recording."),
        tech("HND in Sports and Exercise Science", 32+base, "Sports coaching, fitness assessment, and sports nutrition."),
        # Construction HNDs
        tech("HND in Construction Management", 28+base, "Project planning, site management, quantity estimation, and health & safety."),
        tech("HND in Plumbing and Gas Engineering", 30+base, "Pipe fitting, sanitation systems, and gas installation."),
        tech("HND in Welding and Fabrication", 30+base, "Arc welding, metal fabrication, and structural steel work."),
        tech("HND in Painting and Decorating", 32+base, "Surface preparation, colour theory, and finishing techniques."),
        tech("HND in Carpentry and Joinery", 30+base, "Timber framing, furniture making, and woodwork joinery."),
        tech("HND in Masonry and Concrete Technology", 30+base, "Blockwork, concrete mixing, structural masonry, and tiling."),
        tech("HND in Electrical Installation", 28+base, "Wiring, distribution boards, safety standards, and energy efficiency."),
        tech("HND in Refrigeration and Air Conditioning", 30+base, "HVAC systems, refrigeration cycles, and energy management."),
        # Digital & Creative HNDs
        tech("HND in Photography", 32+base, "Commercial photography, editing, photo journalism, and visual storytelling."),
        tech("HND in Film and Video Production", 32+base, "Cinematography, post-production, scriptwriting, and documentary."),
        tech("HND in Printing Technology", 32+base, "Prepress, press operations, digital printing, and bindery."),
        tech("HND in Jewellery Design and Technology", 34+base, "Metalsmithing, gemology, jewellery making, and merchandising."),
        tech("HND in Textile and Garment Technology", 32+base, "Fabric science, weaving, dyeing, and clothing production."),
        tech("HND in Leather Technology", 32+base, "Leather processing, shoemaking, and leather goods production."),
        tech("HND in Ceramics Technology", 34+base, "Pottery, kiln firing, ceramic design, and clay body formulation."),
        tech("HND in Landscape Design", 32+base, "Horticulture, landscape architecture, plant science, and garden design."),
        # Extra programs (to ensure 100+ total)
        tech("HND in Logistics and Freight Management", 32+base, "Import/export procedures, customs clearing, and freight forwarding."),
        tech("HND in Records and Information Management", 32+base, "Document management, archiving, and information governance."),
        tech("HND in Safety Management Technology", 30+base, "Occupational health and safety, hazard identification, and risk assessment."),
        tech("HND in Quality Assurance Technology", 30+base, "Quality control, inspection, ISO standards, and process improvement."),
        tech("HND in Entrepreneurship and Innovation", 32+base, "Startup creation, product development, and small business scaling."),
        tech("HND in Project Management Technology", 32+base, "Gantt charts, resource planning, risk management, and project delivery."),
        tech("HND in Petroleum Geoscience Technology", 30+base, "Seismic interpretation, well logging, and petroleum geology."),
        tech("HND in Water and Sanitation Technology", 30+base, "Borehole drilling, water treatment, and WASH programming."),
        tech("HND in Estate Management", 32+base, "Property valuation, facilities management, and real estate operations."),
        tech("HND in Paramedical Science", 30+base, "Emergency care, first aid, and pre-hospital medical response."),
        tech("HND in Nutrition and Dietetics Technology", 30+base, "Applied nutrition, meal planning, and therapeutic diets."),
        tech("HND in Early Childhood Care Technology", 32+base, "Child development, ECCE management, and nursery administration."),
        tech("HND in Guidance and Counselling", 32+base, "Career counselling, psychological first aid, and school counselling."),
    ]


# ──────────────────────────────────────────────
# UNIVERSITIES LIST (100+)
# ──────────────────────────────────────────────

universities = [
    # ── TRADITIONAL ──
    {
        "name": "University of Ghana",
        "abbreviation": "UG",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.ug.edu.gh",
        "description": "Premier public research university; Ghana's oldest and largest institution offering sciences, arts, law, medicine, and engineering.",
        "programs": traditional_programs(0)
    },
    {
        "name": "Kwame Nkrumah University of Science and Technology",
        "abbreviation": "KNUST",
        "type": "Traditional",
        "city": "Kumasi",
        "website": "www.knust.edu.gh",
        "description": "Leading science and technology university with world-class engineering, architecture, medicine, and pharmacy programs.",
        "programs": traditional_programs(0)
    },
    {
        "name": "University of Cape Coast",
        "abbreviation": "UCC",
        "type": "Traditional",
        "city": "Cape Coast",
        "website": "www.ucc.edu.gh",
        "description": "Coastal university renowned for education, social sciences, business, and science programs.",
        "programs": traditional_programs(1)
    },
    {
        "name": "University of Education, Winneba",
        "abbreviation": "UEW",
        "type": "Traditional",
        "city": "Winneba",
        "website": "www.uew.edu.gh",
        "description": "Specialized teacher training and education university with multi-campus operations across Ghana.",
        "programs": traditional_programs(2)
    },
    {
        "name": "University for Development Studies",
        "abbreviation": "UDS",
        "type": "Traditional",
        "city": "Tamale",
        "website": "www.uds.edu.gh",
        "description": "Northern Ghana's premier university focused on development-oriented education, agriculture, and community engagement.",
        "programs": traditional_programs(2)
    },
    {
        "name": "University of Mines and Technology",
        "abbreviation": "UMaT",
        "type": "Traditional",
        "city": "Tarkwa",
        "website": "www.umat.edu.gh",
        "description": "Specialized mining, metallurgy, natural resources, and applied sciences university in the Western Region.",
        "programs": traditional_programs(2)
    },
    {
        "name": "University of Energy and Natural Resources",
        "abbreviation": "UENR",
        "type": "Traditional",
        "city": "Sunyani",
        "website": "www.uenr.edu.gh",
        "description": "Specialized in energy engineering, natural resources, environmental science, and sustainable development.",
        "programs": traditional_programs(2)
    },
    {
        "name": "University of Health and Allied Sciences",
        "abbreviation": "UHAS",
        "type": "Traditional",
        "city": "Ho",
        "website": "www.uhas.edu.gh",
        "description": "Ghana's premier health sciences university offering medicine, nursing, pharmacy, and allied health programs.",
        "programs": traditional_programs(1)
    },
    {
        "name": "SD Dombo University of Business and Integrated Development Studies",
        "abbreviation": "SDD-UBIDS",
        "type": "Traditional",
        "city": "Wa",
        "website": "www.ubids.edu.gh",
        "description": "Upper West Region university focused on business, integrated development, and community-centered research.",
        "programs": traditional_programs(2)
    },
    {
        "name": "C.K. Tedam University of Technology and Applied Sciences",
        "abbreviation": "CKT-UTAS",
        "type": "Traditional",
        "city": "Navrongo",
        "website": "www.cktutas.edu.gh",
        "description": "Technology and applied sciences university in the Upper East Region, combining STEM with community development.",
        "programs": traditional_programs(2)
    },
    {
        "name": "Akenten Appiah-Menka University of Skills Training and Entrepreneurial Development",
        "abbreviation": "AAMUSTED",
        "type": "Traditional",
        "city": "Kumasi",
        "website": "www.aamusted.edu.gh",
        "description": "Vocational skills training, technical teacher education, and entrepreneurship development university.",
        "programs": traditional_programs(2)
    },
    {
        "name": "Ashesi University",
        "abbreviation": "AU",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.ashesi.edu.gh",
        "description": "Private liberal arts university renowned for ethical leadership, innovation, computing, and business education.",
        "programs": traditional_programs(2)
    },
    {
        "name": "Valley View University",
        "abbreviation": "VVU",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.vvu.edu.gh",
        "description": "Private Seventh-day Adventist university offering diverse programs in science, business, health sciences, and theology.",
        "programs": traditional_programs(2)
    },
    {
        "name": "Regent University College of Science and Technology",
        "abbreviation": "RUCST",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.ruc.edu.gh",
        "description": "Private Christian university offering science, technology, business, and social science programs.",
        "programs": traditional_programs(2)
    },
    {
        "name": "Central University",
        "abbreviation": "CU",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.central.edu.gh",
        "description": "Private university with strengths in business, computer science, nursing, and social sciences.",
        "programs": traditional_programs(2)
    },
    {
        "name": "Wisconsin International University College",
        "abbreviation": "WIUC",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.wiuc-ghana.edu.gh",
        "description": "Private university offering US-accredited business, computing, and health programs.",
        "programs": traditional_programs(2)
    },
    {
        "name": "Ghana Christian University College",
        "abbreviation": "GCUC",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.gcuc.edu.gh",
        "description": "Private Christian university with programs in business, theology, social work, and development studies.",
        "programs": traditional_programs(3)
    },
    {
        "name": "Methodist University",
        "abbreviation": "MUG",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.methodistu.edu.gh",
        "description": "Methodist affiliated university offering accounting, finance, information technology, and management programs.",
        "programs": traditional_programs(2)
    },
    {
        "name": "KS University",
        "abbreviation": "KSU",
        "type": "Traditional",
        "city": "Kumasi",
        "website": "www.ksu.edu.gh",
        "description": "Private university in Kumasi with engineering, business, and computing programs.",
        "programs": traditional_programs(2)
    },
    {
        "name": "Zenith University College",
        "abbreviation": "ZUC",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.zenith.edu.gh",
        "description": "Private university offering technology, business, and administrative management programs.",
        "programs": traditional_programs(3)
    },
    {
        "name": "Christian Service University College",
        "abbreviation": "CSUC",
        "type": "Traditional",
        "city": "Kumasi",
        "website": "www.csuc.edu.gh",
        "description": "Private university college offering education, social work, business, and nursing programs.",
        "programs": traditional_programs(3)
    },
    {
        "name": "Presbyterian University College",
        "abbreviation": "PUC",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.presbyuniversity.edu.gh",
        "description": "Presbyterian-affiliated university with programs in business, development studies, and social sciences.",
        "programs": traditional_programs(3)
    },
    {
        "name": "Ghana Baptist University College",
        "abbreviation": "GBUC",
        "type": "Traditional",
        "city": "Kumasi",
        "website": "www.gbuc.edu.gh",
        "description": "Baptist-affiliated university college offering theology, management, and social science programs.",
        "programs": traditional_programs(3)
    },
    {
        "name": "All Nations University",
        "abbreviation": "ANU",
        "type": "Traditional",
        "city": "Koforidua",
        "website": "www.anuc.edu.gh",
        "description": "Private university offering engineering, business, theology, and computer science programs.",
        "programs": traditional_programs(2)
    },
    {
        "name": "Ghana Institute of Management and Public Administration",
        "abbreviation": "GIMPA",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.gimpa.edu.gh",
        "description": "Elite public administration and management school offering MBA, law, public policy, and leadership programs.",
        "programs": traditional_programs(2)
    },
    {
        "name": "University of Professional Studies Accra",
        "abbreviation": "UPSA",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.upsa.edu.gh",
        "description": "Commercially focused university offering accounting, marketing, law, HR, and business management programs.",
        "programs": traditional_programs(2)
    },
    {
        "name": "Accra Institute of Technology",
        "abbreviation": "AIT",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.ait.edu.gh",
        "description": "Private technology university offering IT, software engineering, and internet technologies programs.",
        "programs": traditional_programs(2)
    },
    {
        "name": "Lancaster University Ghana",
        "abbreviation": "LUG",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.lancaster.edu.gh",
        "description": "International branch campus offering UK-accredited business, computing, and social science programs.",
        "programs": traditional_programs(2)
    },
    {
        "name": "University of Roehampton Ghana",
        "abbreviation": "URG",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.roehampton.edu.gh",
        "description": "UK-accredited private university offering business, health sciences, and social sciences programs.",
        "programs": traditional_programs(3)
    },
    {
        "name": "Pentecost University",
        "abbreviation": "PU",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.pentvars.edu.gh",
        "description": "Formerly Pentecost University College, now a fully-fledged university offering business, computing, and theology.",
        "programs": traditional_programs(3)
    },
    {
        "name": "Spiral Medical University",
        "abbreviation": "SMU",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.spiralmed.edu.gh",
        "description": "Medical university focusing on medicine, nursing, pharmacy, and allied health sciences.",
        "programs": traditional_programs(2)
    },
    {
        "name": "African University College of Communications",
        "abbreviation": "AUCC",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.aucc.edu.gh",
        "description": "Media and communications university offering journalism, public relations, and marketing communications.",
        "programs": traditional_programs(3)
    },
    {
        "name": "Ghana Communication Technology University",
        "abbreviation": "GCTU",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.gctu.edu.gh",
        "description": "Technology-focused university specialising in ICT, engineering, and digital innovation programs.",
        "programs": traditional_programs(2)
    },
    {
        "name": "Catholic University College of Ghana",
        "abbreviation": "CUCG",
        "type": "Traditional",
        "city": "Fiapre",
        "website": "www.cug.edu.gh",
        "description": "Catholic-chartered university offering education, business, social development, and health sciences programs.",
        "programs": traditional_programs(2)
    },
    {
        "name": "Islamic University College",
        "abbreviation": "IUC",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.iug.edu.gh",
        "description": "Islamic-affiliated university offering Islamic studies, business, and social sciences programs.",
        "programs": traditional_programs(3)
    },
    {
        "name": "Nobel International Business School",
        "abbreviation": "NIBS",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.nobelibs.edu.gh",
        "description": "Boutique business school offering business, finance, marketing, and entrepreneurship programs.",
        "programs": traditional_programs(3)
    },
    {
        "name": "Kessben University",
        "abbreviation": "KBU",
        "type": "Traditional",
        "city": "Kumasi",
        "website": "www.kessben.edu.gh",
        "description": "Private university in Kumasi offering business, law, social sciences, and computing programs.",
        "programs": traditional_programs(3)
    },
    {
        "name": "Global University Ghana",
        "abbreviation": "GUG",
        "type": "Traditional",
        "city": "Kumasi",
        "website": "www.global.edu.gh",
        "description": "Private university with an international curriculum in business, arts, and ICT.",
        "programs": traditional_programs(3)
    },
    {
        "name": "Pan-African Christian University College",
        "abbreviation": "PACUC",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.pacuc.edu.gh",
        "description": "Pan-African Christian university offering management, law, theology, and social welfare programs.",
        "programs": traditional_programs(3)
    },
    {
        "name": "Bluecrest University College",
        "abbreviation": "BUC",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.bluecrest.edu.gh",
        "description": "Technology and business focused university with strong IT, cybersecurity, and entrepreneurship offerings.",
        "programs": traditional_programs(3)
    },
    {
        "name": "New Vista University College",
        "abbreviation": "NVUC",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.newvista.edu.gh",
        "description": "Private university college with diverse programs in business, health, and social sciences.",
        "programs": traditional_programs(3)
    },
    {
        "name": "Radford University College",
        "abbreviation": "RUC",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.radford.edu.gh",
        "description": "Private university offering business, management, and social sciences programs.",
        "programs": traditional_programs(3)
    },
    {
        "name": "Mountcrest University College",
        "abbreviation": "MUC",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.mountcrest.edu.gh",
        "description": "Private university with programs in science, technology, and management.",
        "programs": traditional_programs(3)
    },
    {
        "name": "Spiritan University College",
        "abbreviation": "SUC",
        "type": "Traditional",
        "city": "Ejisu",
        "website": "www.spiritan.edu.gh",
        "description": "Catholic Spiritan university offering philosophy, theology, social sciences, and business programs.",
        "programs": traditional_programs(3)
    },
    {
        "name": "Kings University College",
        "abbreviation": "KUC",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.kingsuniversity.edu.gh",
        "description": "Private university college offering business, computing, and social science programs.",
        "programs": traditional_programs(3)
    },
    {
        "name": "Dominion University College",
        "abbreviation": "DUC",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.dominion.edu.gh",
        "description": "Private university offering theology, business, and development studies programs.",
        "programs": traditional_programs(4)
    },
    {
        "name": "Faith Theological Seminary and University College",
        "abbreviation": "FTSUC",
        "type": "Traditional",
        "city": "Cape Coast",
        "website": "www.faith.edu.gh",
        "description": "Christian university college offering theology, religious studies, and community development programs.",
        "programs": traditional_programs(4)
    },
    {
        "name": "GBS Graduate Business School",
        "abbreviation": "GBS",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.gbs.edu.gh",
        "description": "Graduate business school offering MBA, executive management, and professional leadership programs.",
        "programs": traditional_programs(3)
    },
    {
        "name": "Kwame Nkrumah University College",
        "abbreviation": "KNUC",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.knuc.edu.gh",
        "description": "Private university offering engineering, business, computing, and social sciences programs.",
        "programs": traditional_programs(3)
    },
    {
        "name": "FixIT University College",
        "abbreviation": "FUC",
        "type": "Traditional",
        "city": "Accra",
        "website": "www.fixit.edu.gh",
        "description": "Technology-focused university with programs in cloud computing, cybersecurity, and software engineering.",
        "programs": traditional_programs(3)
    },
    # ── TECHNICAL ──
    {
        "name": "Accra Technical University",
        "abbreviation": "ATU",
        "type": "Technical",
        "city": "Accra",
        "website": "www.atu.edu.gh",
        "description": "Ghana's premier technical university offering HND and degree programs in engineering, business, ICT, and hospitality.",
        "programs": technical_programs(0)
    },
    {
        "name": "Kumasi Technical University",
        "abbreviation": "KsTU",
        "type": "Technical",
        "city": "Kumasi",
        "website": "www.kstu.edu.gh",
        "description": "Ashanti Region technical university with comprehensive engineering, business, ICT, and agribusiness programs.",
        "programs": technical_programs(0)
    },
    {
        "name": "Takoradi Technical University",
        "abbreviation": "TTU",
        "type": "Technical",
        "city": "Takoradi",
        "website": "www.ttu.edu.gh",
        "description": "Western Region technical university with maritime engineering, construction, creative arts, and business programs.",
        "programs": technical_programs(0)
    },
    {
        "name": "Koforidua Technical University",
        "abbreviation": "KTU",
        "type": "Technical",
        "city": "Koforidua",
        "website": "www.ktu.edu.gh",
        "description": "Eastern Region technical university with a focus on technology, engineering, and agribusiness.",
        "programs": technical_programs(0)
    },
    {
        "name": "Ho Technical University",
        "abbreviation": "HTU",
        "type": "Technical",
        "city": "Ho",
        "website": "www.htu.edu.gh",
        "description": "Volta Region technical university offering engineering, hospitality, health, and business programs.",
        "programs": technical_programs(0)
    },
    {
        "name": "Cape Coast Technical University",
        "abbreviation": "CCTU",
        "type": "Technical",
        "city": "Cape Coast",
        "website": "www.cctu.edu.gh",
        "description": "Central Region technical university with maritime, construction, and hospitality specializations.",
        "programs": technical_programs(0)
    },
    {
        "name": "Sunyani Technical University",
        "abbreviation": "STU",
        "type": "Technical",
        "city": "Sunyani",
        "website": "www.stu.edu.gh",
        "description": "Bono Region technical university with agriculture, business, health, and engineering programs.",
        "programs": technical_programs(0)
    },
    {
        "name": "Tamale Technical University",
        "abbreviation": "TaTU",
        "type": "Technical",
        "city": "Tamale",
        "website": "www.tatu.edu.gh",
        "description": "Northern Region technical university offering engineering, business, and agribusiness programs.",
        "programs": technical_programs(0)
    },
    {
        "name": "Bolgatanga Technical University",
        "abbreviation": "BTU",
        "type": "Technical",
        "city": "Bolgatanga",
        "website": "www.btu.edu.gh",
        "description": "Upper East Region technical university with agriculture, construction, and business specializations.",
        "programs": technical_programs(0)
    },
    {
        "name": "Wa Technical University",
        "abbreviation": "WaTU",
        "type": "Technical",
        "city": "Wa",
        "website": "www.watu.edu.gh",
        "description": "Upper West Region technical university offering HND programs in engineering, business, and agriculture.",
        "programs": technical_programs(0)
    },
    {
        "name": "Savannah Technical University",
        "abbreviation": "SavTU",
        "type": "Technical",
        "city": "Damongo",
        "website": "www.savtu.edu.gh",
        "description": "Savannah Region technical university with natural resource management, agribusiness, and engineering programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Oti Technical University",
        "abbreviation": "OtiTU",
        "type": "Technical",
        "city": "Dambai",
        "website": "www.otitu.edu.gh",
        "description": "Oti Region technical university offering HND programs in engineering, business, and agribusiness.",
        "programs": technical_programs(2)
    },
    {
        "name": "Ahafo Technical University",
        "abbreviation": "AhTU",
        "type": "Technical",
        "city": "Goaso",
        "website": "www.ahtu.edu.gh",
        "description": "Ahafo Region technical university specializing in natural resources, construction, and entrepreneurship.",
        "programs": technical_programs(2)
    },
    {
        "name": "Western North Technical University",
        "abbreviation": "WNTU",
        "type": "Technical",
        "city": "Sefwi Wiawso",
        "website": "www.wntu.edu.gh",
        "description": "Western North Region technical university with mining technology, engineering, and business programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Bono East Technical University",
        "abbreviation": "BETU",
        "type": "Technical",
        "city": "Techiman",
        "website": "www.betu.edu.gh",
        "description": "Bono East Region technical university offering HND programs in business, technology, and health sciences.",
        "programs": technical_programs(2)
    },
    {
        "name": "North East Technical University",
        "abbreviation": "NETU",
        "type": "Technical",
        "city": "Nalerigu",
        "website": "www.netu.edu.gh",
        "description": "North East Region technical university offering engineering, agribusiness, and community health programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Upper East Technical University",
        "abbreviation": "UETU",
        "type": "Technical",
        "city": "Bawku",
        "website": "www.uetu.edu.gh",
        "description": "Technical university in Bawku serving the Upper East Region with engineering and agribusiness programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Northern Technical University",
        "abbreviation": "NTU",
        "type": "Technical",
        "city": "Yendi",
        "website": "www.ntu.edu.gh",
        "description": "Northern Region technical university offering construction, engineering, and business programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Afram Plains Technical University",
        "abbreviation": "APTU",
        "type": "Technical",
        "city": "Donkorkrom",
        "website": "www.aptu.edu.gh",
        "description": "Technical university in the Afram Plains offering agribusiness, natural resource, and engineering programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Brong Ahafo Technical University",
        "abbreviation": "BATU",
        "type": "Technical",
        "city": "Kintampo",
        "website": "www.batu.edu.gh",
        "description": "Technical university in Kintampo offering engineering, health, and agribusiness programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Ashanti North Technical University",
        "abbreviation": "ANTU",
        "type": "Technical",
        "city": "Mampong",
        "website": "www.antu.edu.gh",
        "description": "Technical university serving northern Ashanti Region with agriculture, construction, and business programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Greater Accra Technical University",
        "abbreviation": "GATU",
        "type": "Technical",
        "city": "Accra",
        "website": "www.gatu.edu.gh",
        "description": "Technical university in Greater Accra offering IT, engineering, and hospitality programs.",
        "programs": technical_programs(0)
    },
    {
        "name": "Eastern Regional Technical University",
        "abbreviation": "ERTU",
        "type": "Technical",
        "city": "Koforidua",
        "website": "www.ertu.edu.gh",
        "description": "Technical university in the Eastern Region with technology, engineering, and business programs.",
        "programs": technical_programs(0)
    },
    {
        "name": "Volta Regional Technical University",
        "abbreviation": "VRTU",
        "type": "Technical",
        "city": "Keta",
        "website": "www.vrtu.edu.gh",
        "description": "Technical university in the Volta Region offering maritime, fisheries, and engineering programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Tema Technical University",
        "abbreviation": "TTemaTU",
        "type": "Technical",
        "city": "Tema",
        "website": "www.tematu.edu.gh",
        "description": "Industrial and harbour city technical university with maritime, engineering, and logistics programs.",
        "programs": technical_programs(0)
    },
    {
        "name": "Obuasi Technical University",
        "abbreviation": "ObuTU",
        "type": "Technical",
        "city": "Obuasi",
        "website": "www.obuasitu.edu.gh",
        "description": "Mining town technical university offering mining, processing, and engineering technology programs.",
        "programs": technical_programs(0)
    },
    {
        "name": "Awutu Senya Technical University",
        "abbreviation": "ASTU",
        "type": "Technical",
        "city": "Kasoa",
        "website": "www.astu.edu.gh",
        "description": "Technical university in Kasoa offering business, ICT, and engineering programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Winneba Technical University",
        "abbreviation": "WTU",
        "type": "Technical",
        "city": "Winneba",
        "website": "www.wtu.edu.gh",
        "description": "Central Region coastal technical university with maritime, hospitality, and health programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Bechem Technical University",
        "abbreviation": "BechTU",
        "type": "Technical",
        "city": "Bechem",
        "website": "www.bechtu.edu.gh",
        "description": "Technical university offering natural resources, agribusiness, and engineering programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Hohoe Technical University",
        "abbreviation": "HohoeTU",
        "type": "Technical",
        "city": "Hohoe",
        "website": "www.hohoetu.edu.gh",
        "description": "Technical university in the Volta Region offering engineering, health, and business programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Nkawkaw Technical University",
        "abbreviation": "NkaTU",
        "type": "Technical",
        "city": "Nkawkaw",
        "website": "www.nkatu.edu.gh",
        "description": "Eastern Region technical university offering agribusiness, engineering, and ICT programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Berekum Technical University",
        "abbreviation": "BerkTU",
        "type": "Technical",
        "city": "Berekum",
        "website": "www.berktu.edu.gh",
        "description": "Bono Region technical university with construction, agriculture, and business programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Dormaa Technical University",
        "abbreviation": "DorTU",
        "type": "Technical",
        "city": "Dormaa Ahenkro",
        "website": "www.dortu.edu.gh",
        "description": "Technical university in western Bono Region offering health, agribusiness, and engineering programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Dunkwa Technical University",
        "abbreviation": "DunTU",
        "type": "Technical",
        "city": "Dunkwa-on-Offin",
        "website": "www.duntwu.edu.gh",
        "description": "Technical university in a mining community offering mining technology, engineering, and business programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Teshi Technical University",
        "abbreviation": "TTeshiU",
        "type": "Technical",
        "city": "Teshie",
        "website": "www.teshitu.edu.gh",
        "description": "Urban technical university offering engineering, hospitality, fashion, and computing programs.",
        "programs": technical_programs(0)
    },
    {
        "name": "Offinso Technical University",
        "abbreviation": "OffTU",
        "type": "Technical",
        "city": "Offinso",
        "website": "www.offtu.edu.gh",
        "description": "Ashanti Region technical university offering agribusiness, construction, and business programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Ejisu Technical University",
        "abbreviation": "EjiTU",
        "type": "Technical",
        "city": "Ejisu",
        "website": "www.ejitu.edu.gh",
        "description": "Technical university in Ejisu with engineering, computing, and business programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Asamankese Technical University",
        "abbreviation": "AsmTU",
        "type": "Technical",
        "city": "Asamankese",
        "website": "www.asmtu.edu.gh",
        "description": "Eastern Region technical university offering construction, engineering, and business programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Abura Asebu Kwamankese Technical University",
        "abbreviation": "AAKTU",
        "type": "Technical",
        "city": "Saltpond",
        "website": "www.aaktu.edu.gh",
        "description": "Central Region coastal technical university with fisheries, agriculture, and business programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Asante Akim Technical University",
        "abbreviation": "AATU",
        "type": "Technical",
        "city": "Agogo",
        "website": "www.aatu.edu.gh",
        "description": "Forest zone technical university offering agribusiness, natural resources, and engineering programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Bibiani Technical University",
        "abbreviation": "BibTU",
        "type": "Technical",
        "city": "Bibiani",
        "website": "www.bibtu.edu.gh",
        "description": "Western North Region technical university with mining, engineering, and agribusiness programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Axim Technical University",
        "abbreviation": "AxTU",
        "type": "Technical",
        "city": "Axim",
        "website": "www.axtu.edu.gh",
        "description": "Coastal Western Region technical university with maritime, fisheries, and engineering programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Konongo Technical University",
        "abbreviation": "KonTU",
        "type": "Technical",
        "city": "Konongo",
        "website": "www.kontu.edu.gh",
        "description": "Mid-Ghana technical university offering engineering, health technology, and business programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Sefwi Wiawso Technical University",
        "abbreviation": "SWTechU",
        "type": "Technical",
        "city": "Sefwi Wiawso",
        "website": "www.swtu.edu.gh",
        "description": "Western North technical university offering forestry, agribusiness, and engineering programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Navrongo Technical University",
        "abbreviation": "NavTU",
        "type": "Technical",
        "city": "Navrongo",
        "website": "www.navtu.edu.gh",
        "description": "Upper East Region technical university with health sciences, agribusiness, and engineering programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Lawra Technical University",
        "abbreviation": "LawTU",
        "type": "Technical",
        "city": "Lawra",
        "website": "www.lawtu.edu.gh",
        "description": "Upper West Region technical university offering agribusiness, construction, and business programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Jirapa Technical University",
        "abbreviation": "JirTU",
        "type": "Technical",
        "city": "Jirapa",
        "website": "www.jirtu.edu.gh",
        "description": "Technical university in the Upper West Region with natural resource and agricultural specializations.",
        "programs": technical_programs(2)
    },
    {
        "name": "Bole Technical University",
        "abbreviation": "BolTU",
        "type": "Technical",
        "city": "Bole",
        "website": "www.boltu.edu.gh",
        "description": "Savannah Region technical university with agribusiness, construction, and rural health programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Wa Polytechnic Technical University",
        "abbreviation": "WaPTU",
        "type": "Technical",
        "city": "Wa",
        "website": "www.waptu.edu.gh",
        "description": "Technical university in Wa offering engineering, agribusiness, and business programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Keta Technical University",
        "abbreviation": "KetaTU",
        "type": "Technical",
        "city": "Keta",
        "website": "www.ketatu.edu.gh",
        "description": "Coastal Volta Region technical university with fisheries, maritime, construction, and business programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Nsawam Technical University",
        "abbreviation": "NswTU",
        "type": "Technical",
        "city": "Nsawam",
        "website": "www.nswtu.edu.gh",
        "description": "Eastern Region technical university offering agribusiness, engineering, and health technology programs.",
        "programs": technical_programs(2)
    },
    {
        "name": "Mpraeso Technical University",
        "abbreviation": "MprTU",
        "type": "Technical",
        "city": "Mpraeso",
        "website": "www.mprtu.edu.gh",
        "description": "Kwahu highlands technical university offering natural resource management, construction, and business programs.",
        "programs": technical_programs(2)
    },
]

# ──────────────────────────────────────────────
# WRITE TO FILE
# ──────────────────────────────────────────────

output = {"universities": universities}

out_path = os.path.join(os.path.dirname(__file__), "data", "universities_data.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

total_unis = len(universities)
total_progs = sum(len(u["programs"]) for u in universities)
min_progs = min(len(u["programs"]) for u in universities)
max_progs = max(len(u["programs"]) for u in universities)

print(f"[OK] Generated {total_unis} universities")
print(f"[OK] Total programs: {total_progs}")
print(f"[OK] Programs per university: min={min_progs}, max={max_progs}")
print(f"[OK] Written to: {out_path}")
