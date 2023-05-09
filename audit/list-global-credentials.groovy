//https://stackoverflow.com/a/57952857
def creds = com.cloudbees.plugins.credentials.CredentialsProvider.lookupCredentials(
      com.cloudbees.plugins.credentials.Credentials.class
)
for( c in creds){
  	println(c.id + " has scope "+ c.scope) 
}
