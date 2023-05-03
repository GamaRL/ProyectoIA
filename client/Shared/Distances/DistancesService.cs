using System.Net.Http.Json;

public class DistancesService : IDistancesService
{
  private readonly HttpClient _http;

  public DistancesService(HttpClient http)
  {
    this._http = http;
  }

  public async Task<DistanceMatrixResponse> GetDistanceMatrix(int fileId, bool containsHeaders, List<object> columns, StandarizationMethod method)
  {
    UriBuilder uriBuider = new(new Uri(_http.BaseAddress, $"/{(int)AlgorithmType.DISTANCES}/files/{fileId}/distances"));
    string columnString = string.Join("&", columns.Select(c => $"columns={c}").ToList());
    uriBuider.Query = $"contains_headers={containsHeaders.ToString().ToLower()}&{columnString}&method={(int)method}";
    
    return await this._http.GetFromJsonAsync<DistanceMatrixResponse>(uriBuider.Uri.ToString());
  }
}