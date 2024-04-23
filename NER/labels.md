# Proposals for entities

## STIX 2.1

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

### User Account

NER fields:
* user_id:string
* credential:string
* account_login:string
* display_type:string


## MITRE 

## MISP

