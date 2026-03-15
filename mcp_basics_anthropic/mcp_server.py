from pydantic import Field

from mcp.server.fastmcp import FastMCP

from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR")


# Mock document storage - in a real implementation, this would likely be a database or file storage system
docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.", 
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# TODO: Write a tool to read a doc --> DONE
@mcp.tool(
    name="read_doc_contents",
    description="Reads the contents of a document given its name and returns the contents as a string.",
)

def read_document(
    doc_ids: str = Field(description="The name of the document to read")
):
    if doc_ids in docs:
        return docs[doc_ids]
    else:
        raise ValueError(f"Document '{doc_ids}' not found.")

# TODO: Write a tool to edit a doc --> DONE
@mcp.tool(
    name="edit_doc_contents",
    description="Edits the contents of a document given its name and the string that needs to be updated with a new string.",
)

def edit_document(
    doc_ids: str = Field(description="The name of the document to edit"),
    old_contents: str = Field(description="The existing contents of the document that needs to be replaced"),
    new_contents: str = Field(description="The new contents to replace the existing document contents"),
):
    if doc_ids in docs:
        if old_contents in docs[doc_ids]:
            docs[doc_ids] = docs[doc_ids].replace(old_contents, new_contents)
            return f"Document '{doc_ids}' has been updated."
        else:
            raise ValueError(f"Document '{doc_ids}' does not contain the specified old contents.")
    else:
        raise ValueError(f"Document '{doc_ids}' not found.")

# TODO: Write a resource to return all doc id's --> DONE (DIRECT URI)
@mcp.resource(
    "docs://documents",
    mime_type="application/json", # because the list of doc ids is returned as a JSON array
)
def list_docs() -> list[str]:
    return list(docs.keys())

# TODO: Write a resource to return the contents of a particular doc --> DONE (TEMPLATED URI)
@mcp.resource(
    "docs://documents/{doc_id}", # this is defined in fetch_doc() as an argument.
    mime_type="text/plain", # because only the contents are fetched
)
def fetch_doc(doc_id: str) -> str:
    if doc_id in docs:
        return docs[doc_id]

    else:
        raise ValueError(f"Document '{doc_id}' not found.")

# TODO: Write a prompt to rewrite a doc in markdown format --> DONE
@mcp.prompt(
    name="format",
    description="Rewrites the contents of a document in markdown format.",
)

def format_document(
    doc_id: str = Field(description="The name of the document to format") # Field annotation is optional, but it allows us to add a description for the argument which can be helpful for users of the prompt.
) -> list[base.Message]:
    prompt = f"""
    You are helpful assistant in formatting documents into markdown syntax. The id of the document is {doc_id}

    Add in headers, bullet points, code ticks for any code snippets. Feel free to use the 'edit_document' tool if you need to update the document with the new markdown formatting.
    """

    return [
        base.UserMessage(prompt)
    ]
    
# TODO: Write a prompt to summarize a doc --> DONE
@mcp.prompt(
    name="summarize_doc",
    description="Summarizes the contents of a document.",
)

def summarize_doc(doc_id: str) -> list[base.Message]:
    prompt = f"""
    You are a helpful assistant in summarizing technical documents. The id of the document is {doc_id}.

    Provide a concise summary of the document, highlighting the key points and important details. Use bullet points if necessary. Avoid any emojis.
    """

    return [
        base.UserMessage(prompt)
    ]


if __name__ == "__main__":
    mcp.run(transport="stdio")
