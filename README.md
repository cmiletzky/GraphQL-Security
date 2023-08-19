# GraphQL-Security
this project is POC for securing graphQL architecture
GraphQL is a highly flexible query language that can express complex data requirements easily and in more detail than a traditional REST API.
Our goal is to create a POC for securing this architecture.
In this project, we created a layer that examines a large amount of traffic, based on this traffic this layer learns what legitimate traffic is.
After learning this phase, the module hypothesizes what the original schema should look like.
We create a document of rules that we embedded into the proxy through which the requests will go to the GraphQL server,
according to these rules the proxy will decide if the request is legitimate and then it will forward it to the server, if not, the query will be rejected. 
