# ft.py

_The Financial Supervisory Authority of Norway_ (_Finanstilsynet_ or _FT_) maintains a registry called the _Virksomhetsregister_. This registry has information on all companies and individuals under the FT's supervision. FT provides [an API](https://www.finanstilsynet.no/analyser-og-statistikk/api-for-apne-data/) for interaction with the available data in this registry, and _ft.py_ is a simple tool that extracts all data related to _alternative investment funds_ or _AIFs_.

## How to use

Run the tool like this:

```py
python ft.py
```

The tool then exports multiple JSON files in the `.\data` directory. The latest files are suffixed `_latest`. These files are then imported into your application of choice, e.g. Microsoft Excel or Microsoft Power Query.

## Note on license types

All entities in the registry have one or more _licenses_. These define the type of the entity and its operations. To limit the amount of data to that relevant to AIFs, the tool exports `ALTINVAIF`, `BANK`, `DEPOTNY`, `FINANSKONS`, and `FOAVALIN` by default.

### Available license types

| Code       | Norwegian                                               | English                                                      |
| ---------- | ------------------------------------------------------- | ------------------------------------------------------------ |
| ADMETTREF  | Administrator etter referanseverdiloven                 | Administrator under the Benchmark Act                        |
| ADVOKAT    | Advokat som oppfyller vilkår for eiendomsmegling        | Solicitor, security for estate agency                        |
| AKSFORAGV  | Aksessorisk forsikringsagentvirksomhet                  | Ancillary agent activities                                   |
| ALTINVAIF  | Alternativt investeringsfond (AIF)                      | Alternative investment fund (AIF)                            |
| BANK       | Bank                                                    | Bank                                                         |
| BEMEBETI   | Betalingsforetak med begrenset tillatelse               | Payment service provider with a limited authorisat           |
| BETF       | Betalingsforetak                                        | Payment institution                                          |
| BETUKONS   | Betalingstjenestevirksomhet unntatt konsesjonsplikt     | Payment services exempted from the authorisation requirement |
| DEPOTNY    | Depotmottaker                                           | Depositary                                                   |
| EIEMGL     | Eiendomsmegler                                          | Estate agent                                                 |
| EIEMGLFTK  | Eiendomsmeglingsforetak                                 | Estate agency, Act adopted on 29 June 2007                   |
| EPENGEF    | E-pengeforetak                                          | E-money institution                                          |
| FFOR       | Verdipapirforetak                                       | Investment firm                                              |
| FINANSKONS | Holdingforetak                                          | Holding company                                              |
| FINF       | Finansieringsforetak                                    | Finance company                                              |
| FINSTIFT   | Finansstiftelse                                         | Trust                                                        |
| FOAVALIN   | Forvalter av alternative investeringsfond (AIFM)        | Alternative Investment Fund Manager (AIFM)                   |
| FONINOEI   | Forvalter (nominee) i norske eierregistre               | Nominee in Norwegian securities registers                    |
| FORAGNTFTK | Forsikringsagentforetak                                 | Insurance agency                                             |
| FORMGLFTK  | Forsikringsmeglingsforetak                              | Insurance brokerage firm                                     |
| FREMINKASO | Fremmedinkassoforetak                                   | Agency debt collection on behalf of others                   |
| FVLTSLSKVP | Forvaltningsselskap for verdipapirfond                  | Management company for securities funds                      |
| GFORMGLFTK | Gjenforsikringsmeglingsforetak                          | Reinsurance brokerage firm                                   |
| GJELDSINFO | Gjeldsinformasjonsforetak                               | Debt registry                                                |
| INNPENF    | Innskuddspensjonsforetak                                | Defined contribution pension undertakings                    |
| JURTEIEMGL | Jurist med tillatelse til å drive eiendomsmegling       | Lawyer, security for estate agency                           |
| KOMMPENKAS | Kommunal pensjonskasse mv.                              | Municipal pension fund                                       |
| KREDITTFOR | Kredittforetak                                          | Credit Institution                                           |
| LÅNGARFORM | Registrert låne- og garantiformidler                    | Intermediator of loans and guarantees                        |
| LIVSFORSIK | Livsforsikringsforetak                                  | Life insurance company                                       |
| MARKEDSOP  | Markedsoperatør                                         | Market operator                                              |
| MGLEIEMGLV | Megler i eiendomsmeglingsvirksomhet                     | Broker in estate agency                                      |
| OPPEGENINF | Oppkjøps-/egeninkassoforetak                            | Debt collection agency - purchase and collection             |
| OPPEGENINP | Personlig oppkjøps-/egeninkassotillatelse               | Pers. debt coll. license - purchase and collection           |
| OPPLYSNING | Opplysningsfullmektig                                   | Account information service provider                         |
| PENFOND    | Pensjonsfond                                            | Pension foundation                                           |
| PERSINKASS | Personlig inkassobevilling                              | Personal debt collection license                             |
| PRIVPENKAS | Privat pensjonskasse                                    | Private pension fund                                         |
| REGNSN     | Filial av utenlandsk regnskapsførerselskap (NUF)        | Branch of foreign external accounting firm (NUF)             |
| REGP       | Regnskapsfører                                          | External accountant                                          |
| REGS       | Regnskapsselskap                                        | External accounting firm                                     |
| RETHEIEMGL | Rettshjelper som oppfyller vilkår for eiendomsmegling   | Legal practitioner, security for estate agency               |
| REVP       | Revisor                                                 | Auditor                                                      |
| REVS       | Revisjonsselskap                                        | Audit firm                                                   |
| RSTATMNR   | Statsautorisert revisor                                 | State authorised auditor                                     |
| RSTATUNR   | Statsautorisert revisor uten revisorregisternummer      | State authorised auditor w/o audit register number           |
| SJØTRYGDEL | Sjøtrygdelag                                            | Marine insurance association                                 |
| SKADEFORSI | Skadeforsikringsforetak                                 | Non-life insurance company                                   |
| SPBAST     | Sparebankstiftelse                                      | Savings bank foundation                                      |
| SYSTEINTER | Systematisk internaliserer                              | Systematic internaliser                                      |
| TILAVVIR   | Tilbyder av virksomhetstjenester                        | Company service providers                                    |
| VEOGOPFOVI | Vekslings- og oppbevaringstjenester for virtuell valuta | Virtual currency service providers                           |
| VERDIPAPS  | Verdipapirsentral                                       | Central securities depository                                |
| VERPAPFOND | Verdipapirfond                                          | Securities fund                                              |
