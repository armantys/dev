import React, { useState, useEffect } from 'react';
import { Col, Card, CardTitle, Button, Row, Modal, ModalHeader, ModalBody, ModalFooter, Form, FormGroup, Label, Input} from 'reactstrap';
import { collection, query, limit, getDocs, doc as firestoreDoc, addDoc, Timestamp, orderBy } from 'firebase/firestore';
import { db } from '../../components/firebase/Firebase';
import ComponentCard from '../../components/ComponentCard';

const StarterKit = () => {
    const [modelName, setModelName] = useState(null);
    const [modelVersion, setModelVersion] = useState(null);
    const [datafps, setdatafps] = useState(null);
    const [dataLearningRate, setDataLearninRate] = useState(null);
    const [dataSeuil, setDataSeuil] = useState(null);
    const [modal, setModal] = useState(false);
    const [dataAcquisition, setDataAcquisition] = useState([]);
    const [dataApplication, setDataApplication] = useState([]);
    const [dataModelIA, setDataModelIA] = useState([]);
    const [modalHistorique, setModalHistorique] = useState(false);
    const [modalApplication, setModalApplication] = useState(false);
    const [dureeSalves, setDureeSalves] = useState(null); // Déclarer dureeSalves
    const [nbImages, setNbImages] = useState(null); // Déclarer nbImages
    const [numeroVersion, setNumeroVersion] = useState(null); // Déclarer numeroVersion
    const [templateWeb, setTemplateWeb] = useState(''); // Déclarer templateWeb avec une chaîne vide par défaut
    const [versionNode, setVersionNode] = useState(''); // Déclarer versionNode avec une chaîne vide par défaut

    const toggle = () => {
        setModal(!modal);
    };

  
    const toggleHistorique = () => {
        setModalHistorique(!modalHistorique);
    };

    const toggleApplication = () => {
        setModalApplication(!modalApplication);
    };


    useEffect(() => {
        setModelName(dataModelIA.nom_modele);
        setModelVersion(dataModelIA.version);
        setdatafps(dataModelIA.nom_modele);
        setDataLearninRate(dataModelIA.version);
        setDataSeuil(dataModelIA.version);
    }, [dataModelIA]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const acquisitionDocRef = firestoreDoc(db, 'BDD_pub_nopub', 'acquisition');
                const historiqueCollectionRef = collection(acquisitionDocRef, 'historique');
                const historiqueQuery = query(historiqueCollectionRef, orderBy('hp_acquisition.timestamp', 'desc'), limit(1)); // Tri par timestamp descendant
                const historiqueQuerySnapshot = await getDocs(historiqueQuery);
                if (!historiqueQuerySnapshot.empty) {
                const historiqueDoc = historiqueQuerySnapshot.docs[0];
                const historiqueData = historiqueDoc.data().hp_acquisition;
                setDataAcquisition(historiqueData);
                } else {
                console.log('Aucun document trouvé dans la collection "historique"');
                }
            } catch (error) {
                console.error('Erreur lors de la récupération des données :', error);
            }
        };
        fetchData();
    }, []);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const applicationDocRef = firestoreDoc(db, 'BDD_pub_nopub', 'application');
                const versionCollectionRef = collection(applicationDocRef, 'version');
                const versionQuery = query(versionCollectionRef,orderBy('timestamp', 'desc'), limit(1));
                const versionQuerySnapshot = await getDocs(versionQuery);
                if (!versionQuerySnapshot.empty) {
                const versionDoc = versionQuerySnapshot.docs[0];
                const versionData = versionDoc.data();
                setDataApplication(versionData);
                } else {
                console.log('Aucun document trouvé dans la collection "version"');
                }
            } catch (error) {
                console.error('Erreur lors de la récupération des données :', error);
            }
        };
        fetchData();
    }, []);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const applicationDocRef = firestoreDoc(db, 'BDD_pub_nopub', 'modele_IA');
                const versionCollectionRef = collection(applicationDocRef, 'version');
                const versionQuery = query(versionCollectionRef, orderBy ('timestamp','desc'), limit(1));
                const versionQuerySnapshot = await getDocs(versionQuery);
                if (!versionQuerySnapshot.empty) {
                const versionDoc = versionQuerySnapshot.docs[0];
                const versionData = versionDoc.data();
                setDataModelIA(versionData);
                } else {
                console.log('Aucun document trouvé dans la collection "version"');
                }
            } catch (error) {
                console.error('Erreur lors de la récupération des données :', error);
            }
        };
        fetchData();
    }, []);

    const handleModelNameChange = (e) => {
        setModelName(e.target.value);
    };

    const handleModelVersionChange = (e) => {
        setModelVersion(e.target.value);
    };

    const handleFpsChange = (e) => {
        setdatafps(e.target.value);
    };

    const handleLearningRateChange = (e) => {
        setDataLearninRate(e.target.value);
    };

    const handleSeuilDecisionChange = (e) => {
        setDataSeuil(e.target.value);
    };

    const renderObject = (object) => {
        return (
            <ul style={{ listStyleType: 'none', paddingLeft: 0 }}>
                {Object.entries(object).map(([subKey, subValue]) => (
                    <li key={subKey}>
                        <strong>{subKey}:</strong> {typeof subValue === 'object' ? renderObject(subValue) : subValue}
                    </li>
                ))}
            </ul>
        );
    };

    const handleSubmitModelIA = async () => {
        try {
            // Construire les données à enregistrer dans la base de données
            const data = {
                hp: {
                    fps: datafps,
                    learning_rate: dataLearningRate
                },
                infos_modele: {
                    nom_modele: modelName,
                    version: modelVersion
                },
                seuil_decision: dataSeuil,
                timestamp: Timestamp.now()
            };


            // Ajouter un nouveau document avec les données construites dans la collection appropriée
            const docRef = await addDoc(collection(db, 'BDD_pub_nopub', 'modele_IA', 'version'), data);
            console.log('Document ajouté avec l\'ID : ', docRef.id);
            window.location.reload(); // Recharge la page
        } catch (error) {
            console.error('Erreur lors de l\'ajout du document : ', error);
        }
    };


    const handleSubmitHistorique = async () => {
        try {
            const historiqueCollectionRef = collection(db, 'BDD_pub_nopub', 'acquisition', 'historique');
            await addDoc(historiqueCollectionRef, {
                hp_acquisition: {
                    duree_salves: dureeSalves,
                    nb_images: nbImages,
                    timestamp: Timestamp.now() // Assurez-vous d'importer Timestamp depuis firebase/firestore
                },

            });
            toggleHistorique(); // Ferme le modal après soumission
            // Rafraîchir les données si nécessaire
            window.location.reload(); // Recharge la page
        } catch (error) {
            console.error('Erreur lors de l\'ajout du document :', error);
        }
        };

    const handleSubmitApplication = async () => {
        try {
            // Construire les données à enregistrer dans la base de données
            const data = {
                numero_version: numeroVersion,
                template_web: templateWeb,
                timestamp: Timestamp.now(),
                version_node: versionNode
            };
        
            // Ajouter un nouveau document avec les données construites dans la collection appropriée
            const docRef = await addDoc(collection(db, 'BDD_pub_nopub', 'application', 'version'), data);
            console.log('Document ajouté avec l\'ID : ', docRef.id);
            window.location.reload(); // Recharge la page
        } catch (error) {
            console.error('Erreur lors de l\'ajout du document : ', error);
        }
    };

    return (
        <>
            {dataAcquisition && dataApplication && dataModelIA && (
                <div>
                    <Row className="success" lg="12">
                        <Col md="6" lg="4">
                            <Card body className="text-center" style={{ display: 'flex', flexGrow: '1', justifyContent: 'space-between', height: '450px' }}>
                                <CardTitle tag="h3">historique acquisition</CardTitle>
                                {/* Vérifier si les données d'acquisition existent et si elles ne sont pas vides */}
                                {dataAcquisition && Object.entries(dataAcquisition).map(([key, value]) => (
                                key !== 'timestamp' &&
                                // Afficher chaque clé et valeur
                                <div style={{ marginTop: '10px' }} key={key}>
                                    <strong style={{ color: typeof value === 'object' ? '#333' : '#000' }}>{key}:</strong> {value}
                                </div>
                                ))}
                                {/* Afficher le timestamp */}
                                <div>
                                {dataAcquisition && dataAcquisition.timestamp && (
                                <div>
                                    {new Date(dataAcquisition.timestamp.seconds * 1000 + dataAcquisition.timestamp.nanoseconds / 1000000).toLocaleString()}
                                </div>
                                )}
                                {/* Bouton de modification */}
                                <Button color="light-danger" className="custom-button" style={{ marginTop: '50px' }} onClick={toggleHistorique.bind(null)}>modifier</Button>
                                </div>
                            </Card>
                        </Col>
                        <Col md="6" lg="4">
                            <Card body className="text-center" style={{display:'flex', flexGrow: '1',justifyContent: 'space-between', height: '450px' }}>
                                <CardTitle tag="h3">version application</CardTitle>
                                {Object.entries(dataApplication).map(([key, value]) => (
                                key !== 'timestamp' &&
                                <div style={{ marginTop: '10px' }} key={key}>
                                    <strong style={{ color: typeof subValue === 'object' ? '#333' : '#000' }}>{key}:</strong> {value}
                                </div>
                                ))}
                                <div>
                                {dataApplication.timestamp && (
                                    <div>
                                    {new Date(dataApplication.timestamp.seconds * 1000 + dataApplication.timestamp.nanoseconds / 1000000).toLocaleString()}
                                    </div>
                                )}
                                <Button color="light-danger" className="custom-button" style={{ marginTop: '50px' }} onClick={toggleApplication.bind(null)}>modifier</Button>
                                </div>
                            </Card>
                        </Col>
                        <Col md="6" lg="4">
                            <Card body className="text-center" style={{display:'flex', flexGrow: '1',justifyContent: 'space-between', height: '450px' }}>
                                <CardTitle tag="h3">Version modèle IA</CardTitle>
                                {Object.entries(dataModelIA).map(([key, value]) => (
                                    key !== 'timestamp' &&
                                    <div style={{ marginTop: '10px' }} key={key}>
                                        <strong style={{ color: typeof key === 'object' ? '#333' : '#000' }}>{key}:</strong> {typeof value === 'object' ? renderObject(value) : value}
                                    </div>
                                ))}
                                <div>
                                    {dataModelIA.timestamp && (
                                    <div style={{ marginTop: '20px' }}>
                                        {new Date(dataModelIA.timestamp.seconds * 1000 + dataModelIA.timestamp.nanoseconds / 1000000).toLocaleString()}
                                    </div>
                                    )}
                                    <Modal isOpen={modal} toggle={toggle.bind(null)}>
                                        <ModalHeader toggle={toggle.bind(null)}>Modifier les informations du modèle IA</ModalHeader>
                                        <ModalBody>
                                            <Col md="12">
                                                <ComponentCard title="Formulaire">
                                                    <Form>
                                                        <FormGroup>
                                                            <Label htmlFor="fps">FPS</Label>
                                                            <Input
                                                                type="number"
                                                                id="fps"
                                                                value={datafps || ''}
                                                                onChange={handleFpsChange}
                                                            />
                                                        </FormGroup>
                                                        <FormGroup>
                                                            <Label htmlFor="learningRate">Learning Rate</Label>
                                                            <Input
                                                                type="number"
                                                                id="learningRate"
                                                                value={dataLearningRate || ''}
                                                                onChange={handleLearningRateChange}
                                                            />
                                                        </FormGroup>
                                                        <FormGroup>
                                                            <Label htmlFor="modelName">Nom du modèle</Label>
                                                            <Input
                                                                type="text"
                                                                id="modelName"
                                                                value={modelName || ''}
                                                                onChange={handleModelNameChange}
                                                            />
                                                        </FormGroup>
                                                        <FormGroup>
                                                            <Label htmlFor="modelVersion">Version du modèle</Label>
                                                            <Input
                                                                type="number"
                                                                id="modelVersion"
                                                                value={modelVersion|| ''}
                                                                onChange={handleModelVersionChange}
                                                            />
                                                        </FormGroup>
                                                        <FormGroup>
                                                            <Label htmlFor="seuilDecision">Seuil de décision</Label>
                                                            <Input
                                                                type="text"
                                                                id="seuilDecision"
                                                                value={dataSeuil || ''}
                                                                onChange={handleSeuilDecisionChange}
                                                            />
                                                        </FormGroup>
                                                    </Form>
                                                </ComponentCard>
                                            </Col>
                                        </ModalBody>
                                        <ModalFooter>
                                            <Button color="primary" onClick={handleSubmitModelIA}>Soumettre</Button>
                                            <Button color="secondary" onClick={toggle.bind(null)}>Annuler</Button>
                                        </ModalFooter>
                                    </Modal>
                                    {/*Modal for Historique acquisition*/} 
                                    <Modal isOpen={modalHistorique} toggle={toggleHistorique}>
                                        <ModalHeader toggle={toggleHistorique}>Modifier l&apos;historique d&apos;acquisition</ModalHeader>
                                        <ModalBody>
                                            <Form>
                                                <FormGroup>
                                                    <Label htmlFor="dureeSalves">Durée des salves</Label>
                                                    <Input
                                                        type="number"
                                                        id="dureeSalves"
                                                        value={dureeSalves || ''}
                                                        onChange={(e) => setDureeSalves(e.target.value)}
                                                    />
                                                </FormGroup>
                                                <FormGroup>
                                                    <Label htmlFor="nbImages">Nombre d&apos;images</Label>
                                                    <Input
                                                        type="number"
                                                        id="nbImages"
                                                        value={nbImages || ''}
                                                        onChange={(e) => setNbImages(e.target.value)}
                                                    />
                                                </FormGroup>
                                            </Form>
                                        </ModalBody>
                                        <ModalFooter>
                                            <Button color="primary" onClick={handleSubmitHistorique}>Soumettre</Button>
                                            <Button color="secondary" onClick={toggleHistorique}>Annuler</Button>
                                        </ModalFooter>
                                    </Modal>

                                    {/* Modal for Version application*/}
                                    <Modal isOpen={modalApplication} toggle={toggleApplication}>
                                        <ModalHeader toggle={toggleApplication}>Modifier la version de l&apos;application</ModalHeader>
                                        <ModalBody>
                                            <Form>
                                                <FormGroup>
                                                    <Label htmlFor="numeroVersion">Numéro de version</Label>
                                                    <Input
                                                        type="number"
                                                        id="numeroVersion"
                                                        value={numeroVersion || ''}
                                                        onChange={(e) => setNumeroVersion(e.target.value)}
                                                    />
                                                </FormGroup>
                                                <FormGroup>
                                                    <Label htmlFor="templateWeb">Template web</Label>
                                                    <Input
                                                        type="text"
                                                        id="templateWeb"
                                                        value={templateWeb || ''}
                                                        onChange={(e) => setTemplateWeb(e.target.value)}
                                                    />
                                                </FormGroup>
                                                <FormGroup>
                                                    <Label htmlFor="versionNode">Version Node</Label>
                                                    <Input
                                                        type="text"
                                                        id="versionNode"
                                                        value={versionNode || ''}
                                                        onChange={(e) => setVersionNode(e.target.value)}
                                                    />
                                                </FormGroup>
                                            </Form>
                                        </ModalBody>
                                        <ModalFooter>
                                            <Button color="primary" onClick={handleSubmitApplication}>Soumettre</Button>
                                            <Button color="secondary" onClick={toggleApplication}>Annuler</Button>
                                        </ModalFooter>
                                    </Modal>
                                    <Button style={{ marginTop: '50px' }} color="light-danger" className="custom-button" onClick={toggle.bind(null)}>Modifier</Button>
                                </div>
                            </Card>
                        </Col>
                    </Row>
                    <div className="text-center" style={{ marginBottom: '20px'}}>
                        <iframe
                            width="560"
                            height="315"
                            src="https://www.youtube.com/embed/jCY6DH8F4oc"
                            title="CRUD Tutorial Using React + Firebase | Firebase 9 and Firestore Tutorial"
                            frameBorder="0"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                            allowFullScreen
                            style={{ marginTop: '20px' }}
                        />
                    </div>
                </div>
            )}
        </>
    );
};

export default StarterKit;
