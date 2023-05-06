using System.Net.Http.Json;

public class DistancesService : IDistancesService
{
  private readonly HttpClient _http;

  public DistancesService(HttpClient http)
  {
    this._http = http;
  }

  public async Task<DistanceMatrixResponse> GetDistanceMatrix(int fileId, bool containsHeaders, List<object> columns, DistanceMetric metric, StandarizationMethod standarization)
  {
    string path = GetDistancesRequestUrl(fileId, false, containsHeaders, columns, metric, standarization);
    
    return await this._http.GetFromJsonAsync<DistanceMatrixResponse>(path);
  }

  public string GetDistancesRequestUrl(int fileId, bool download, bool containsHeaders, List<object> columns, DistanceMetric metric, StandarizationMethod standarization)
  {
    UriBuilder uriBuider = new(new Uri(_http.BaseAddress, $"/{(int)AlgorithmType.DISTANCES}/files/{fileId}/distances"));
    string columnString = string.Join("&", columns.Select(c => $"columns={c}").ToList());

    uriBuider.Query = $"contains_headers={containsHeaders.ToString().ToLower()}&{columnString}&standarization={(int)standarization}&download={download.ToString().ToLower()}&metric={(int)metric}";

    return uriBuider.Uri.ToString();
  }
}