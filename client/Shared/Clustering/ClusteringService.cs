using System.Net.Http.Json;

public class ClusteringService : IClusteringService
{
  private readonly HttpClient _http;

  public ClusteringService(HttpClient http)
  {
    this._http = http;
  }

  public async Task<CorrelationAnalysisResponse> GetCorrelationAnalysis(int fileId, bool containsHeaders)
  {
    UriBuilder uriBuilder = new(new Uri(_http.BaseAddress, $"/{(int)AlgorithmType.CLUSTERING}/files/{fileId}/dimensionality"));
    uriBuilder.Query = $"contains_headers={containsHeaders.ToString().ToLower()}";

    return await this._http.GetFromJsonAsync<CorrelationAnalysisResponse>(uriBuilder.Uri.ToString());
  }

  public string GetCorrelationUrl(CorrelationAnalysisResponse response)
  {
    UriBuilder uriBuilder = new(new Uri(_http.BaseAddress, $"/{(int)AlgorithmType.CLUSTERING}/images/{response.MapFileName}/"));
    Console.WriteLine(uriBuilder.Path);
    string baseAddress = _http.BaseAddress.ToString();
    baseAddress = baseAddress.Substring(0, baseAddress.Length - 1);
    return Path.Join(baseAddress, uriBuilder.Path);
  }
}