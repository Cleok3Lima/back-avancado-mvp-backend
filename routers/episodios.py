# routers/episodios.py
# Rotas que consomem a API pública do Rick and Morty (https://rickandmortyapi.com)

import httpx
from fastapi import APIRouter, HTTPException, Query

# URL base da API externa
RICK_MORTY_API = "https://rickandmortyapi.com/api"

router = APIRouter(
    prefix="/episodios",
    tags=["Episódios"],
)


@router.get("/", summary="Listar episódios com paginação e filtro por temporada")
async def listar_episodios(
    page: int = Query(1, ge=1, description="Número da página"),
    season: int = Query(None, ge=1, le=9, description="Filtrar por temporada (1–9)"),
):
    """
    Retorna uma lista paginada de episódios buscada diretamente da API do Rick and Morty.
    Quando 'season' é fornecido, retorna todos os episódios daquela temporada (sem paginação).
    """
    params = {"page": page}
    if season is not None:
        params["episode"] = f"S{season:02d}"

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{RICK_MORTY_API}/episode", params=params)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Erro ao buscar episódios na API do Rick and Morty"
        )

    return response.json()


@router.get("/{episode_id}", summary="Buscar detalhes de um episódio com personagens")
async def buscar_episodio(episode_id: int):
    """
    Retorna os detalhes de um episódio específico, incluindo os dados completos
    de todos os personagens que aparecem nele (resolvendo as URLs da API).
    """
    async with httpx.AsyncClient() as client:
        # Busca o episódio pelo ID
        ep_response = await client.get(f"{RICK_MORTY_API}/episode/{episode_id}")

        if ep_response.status_code == 404:
            raise HTTPException(status_code=404, detail="Episódio não encontrado")

        if ep_response.status_code != 200:
            raise HTTPException(
                status_code=ep_response.status_code,
                detail="Erro ao buscar episódio na API do Rick and Morty"
            )

        episodio = ep_response.json()

        # A API retorna uma lista de URLs de personagens, ex:
        # ["https://rickandmortyapi.com/api/character/1", ...]
        # Precisamos extrair os IDs e buscar todos de uma vez
        character_urls = episodio.get("characters", [])
        character_ids = [url.split("/")[-1] for url in character_urls]

        personagens = []
        if character_ids:
            # Se há apenas 1 personagem, a API retorna um objeto; se há vários, retorna lista
            ids_str = ",".join(character_ids)
            char_response = await client.get(f"{RICK_MORTY_API}/character/{ids_str}")

            if char_response.status_code == 200:
                data = char_response.json()
                # Garante que o resultado seja sempre uma lista
                personagens = data if isinstance(data, list) else [data]

    # Retorna o episódio enriquecido com os dados dos personagens
    return {
        **episodio,
        "characters": personagens,
    }
