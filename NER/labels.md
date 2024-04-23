# Proposals for entities

## STIX 2.1

## SDO

### Identity
Identities can represent actual individuals, organizations, or groups (e.g., ACME, Inc.) as well as classes of individuals, organizations, systems or groups (e.g., the finance sector).

 
The Identity SDO can capture basic identifying information, contact information, and the sectors that the Identity belongs to. Identity is used in STIX to represent, among other things, targets of attacks, information sources, object creators, and threat actor identities.

NER fields:
* name: string required
* identity_class: optional from enumeration
* sectors: optional from enumeration

identity class enumeraiton: 

individual, group, system, organization, class, unknown

secotrs class enumeration:

agriculture, aerospace, automotive, chemical, commercial, communications, construction, defense, education, energy, entertainment, financial-services, government (emergency-services, government-local, government-national, government-public-services,  government-regional), healthcare, hospitality-leisure, infrastructure (dams, nuclear, water), insurance, manufacturing, mining, non-profit, pharmaceuticals, retail, technology, telecommunications, transportation, utilities

The user can assign an identity with a name but also be able to choose the enumerations as optionak.

## Observables

* AlternateDataStream
* ArchiveExt
* Artifact
* AutonomousSystem
* Directory
* DomainName
* EmailAddress
* EmailMIMEComponent
* EmailMessage
* File
* HTTPRequestExt
* ICMPExt
* IPv6Address
* MACAddress
* Mutex
* NTFSExt
* NetworkTraffic
* PDFExt
* Process
* RasterImageExt
* SocketExt
* Software
* TCPExt
* UNIXAccountExt
* URL
* UserAccount
* WindowsPEBinaryExt
* WindowsPEOptionalHeaderType
* WindowsPESection
* WindowsProcessExt
* WindowsRegistryKey
* WindowsRegistryValueType
* WindowsServiceExt
* X509Certificate
* X509V3ExtensionsType
* CustomObservable: NO

### URL
NER fields:
* value: string required

regexable: YES

### IPv4Address

NER fields:
* value: string required

### User Account

NER fields:
* user_id:string
* credential:string
* account_login:string
* display_type:string


## MITRE 

## MISP

