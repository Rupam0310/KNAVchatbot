import os
import streamlit as st
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType
from azure_openai import *  # Assuming you have OpenAI helper functions like create_prompt() and generate_answer
from config import *  # Ensure you have correct environment variables or .env for the configuration

st.header('Search Engine - Document')

user_input = st.text_input('Enter your question here:', 
                           'Hello')

if st.button('Submit'):

    # Use environment variables for service and key
    service_name = searchservice  # Retrieved from .env or config.py
    key = searchkey  # Retrieved from .env or config.py

    # Ensure the correct endpoint format
    endpoint = service_name
    index_name = index  # Make sure this is properly set in your environment or config.py

    # Initialize Azure Search client
    azure_credential = AzureKeyCredential(key)
    search_client = SearchClient(endpoint=endpoint,
                                        index_name=index_name,
                                        credential=azure_credential)

    # Set the field names for the search results
    KB_FIELDS_CONTENT = os.environ.get("KB_FIELDS_CONTENT", "content")
    KB_FIELDS_CATEGORY = os.environ.get("KB_FIELDS_CATEGORY", category)
    KB_FIELDS_SOURCEPAGE = os.environ.get("KB_FIELDS_SOURCEPAGE", "sourcepage")

    exclude_category = None

    # Search query
    print("Searching:", user_input)
    print("-------------------")
    
    # Apply category filter if needed
    filter = f"category ne '{exclude_category.replace("'", "''")}'" if exclude_category else None
    
    # Execute the search query with semantic settings
    r = search_client.search(user_input, 
                             filter=filter,
                             query_type=QueryType.SEMANTIC, 
                             query_language="en-us", 
                             query_speller="lexicon", 
                             semantic_configuration_name="default", 
                             top=3)
    
    # Process the search results
    results = []
    for doc in r:
        # Safely access the sourcepage and content
        sourcepage = doc.get(KB_FIELDS_SOURCEPAGE, "Unknown Source")
        content = doc.get(KB_FIELDS_CONTENT, "No Content Available")
        
        # Format results
        results.append(f"{sourcepage}: {content.replace('\n', '').replace('\r', '')}")
    
    content = "\n".join(results)

    # Extract references from the search results
    references = [result.split(":")[0] for result in results]
    st.markdown("### References:")
    st.write(" , ".join(set(references)))

    # Prepare prompt for OpenAI or Azure OpenAI
    conversation = [{"role": "system", "content": "Assistant is a great language model formed by OpenAI."}]
    prompt = create_prompt(content, user_input)  # Assuming you have this function defined
    conversation.append({"role": "assistant", "content": prompt})
    conversation.append({"role": "user", "content": user_input})
    
    # Generate the answer using OpenAI or Azure OpenAI
    reply = generate_answer(conversation)  # Assuming you have this function defined

    # Display the answer in Streamlit
    st.markdown("### Answer is:")
    st.write(reply)
