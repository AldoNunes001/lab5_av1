LISTAR TODOS OS PRODUTOS
{
  allProducts {
    id
    title
    unitPrice
  }
}

CRIAR NOVO PRODUTO
mutation {
  createProduct(
    title: "Novo Produto"
    slug: "novo-produto"
    unitPrice: 29.99
    inventory: 100
    collectionId: 1
  ) {
    product {
      id
      title
      unitPrice
      inventory
    }
  }
}

DETALHES DE UM PRODUTO
{
  product(id: 1) {
    id
    title
    description
    unitPrice
    inventory
    lastUpdate
    collection {
      id
      title
    }
    promotions {
      id
      description
      discount
    }
  }
}

ATUALIZAR UM PRODUTO
mutation {
  updateProduct(
    id: 1
    title: "Produto Atualizado"
    inventory: 150
  ) {
    product {
      id
      title
      inventory
    }
  }
}

DELETAR UM PRODUTO
mutation {
  deleteProduct(id: 1) {
    success
  }
}

