using System.Net.Http.Json;

public class ClusteringService : IClusteringService
{
  private readonly HttpClient _http;

  public ClusteringService(HttpClient http)
  {
    this._http = http;
  }

  public async Task<string> GetAgglomarativeClustersImg(int fileId, bool containsHeaders, List<object> columns, StandarizationMethod standarization, DistanceMetric metric)
  {
    UriBuilder uriBuilder = new(new Uri(_http.BaseAddress, $"/{(int)AlgorithmType.CLUSTERING}/files/{fileId}/agglomerative/img"));
    string columnString = string.Join("&", columns.Select(c => $"columns={c}").ToList());

    uriBuilder.Query = $"contains_headers={containsHeaders.ToString().ToLower()}&{columnString}&standarization={(int)standarization}&metric={(int)metric}";

    return await this._http.GetFromJsonAsync<string>(uriBuilder.Uri.ToString());
  }

  public async Task<List<ClusterResponse>> GetPartitionalClusters(int fileId, bool containsHeaders, List<object> columns, StandarizationMethod standarization, DistanceMetric metric, int noClusters, bool download = false)
  {
    UriBuilder uriBuider = new(new Uri(_http.BaseAddress, $"/{(int)AlgorithmType.CLUSTERING}/files/{fileId}/partitional"));
    string columnString = string.Join("&", columns.Select(c => $"columns={c}").ToList());

    uriBuider.Query = $"contains_headers={containsHeaders.ToString().ToLower()}&{columnString}&standarization={(int)standarization}&download={download.ToString().ToLower()}&metric={(int)metric}&no_clusters={noClusters}";

    return await this._http.GetFromJsonAsync<List<ClusterResponse>>(uriBuider.Uri.ToString());
  }

  public async Task<CorrelationAnalysisResponse> GetCorrelationAnalysis(int fileId, bool containsHeaders)
  {
    UriBuilder uriBuilder = new(new Uri(_http.BaseAddress, $"/{(int)AlgorithmType.CLUSTERING}/files/{fileId}/dimensionality"));
    uriBuilder.Query = $"contains_headers={containsHeaders.ToString().ToLower()}";

    return await this._http.GetFromJsonAsync<CorrelationAnalysisResponse>(uriBuilder.Uri.ToString());
  }

  public string GetImageUrl(string resource)
  {
    UriBuilder uriBuilder = new(new Uri(_http.BaseAddress, $"/{(int)AlgorithmType.CLUSTERING}/images/{resource}/"));
    string baseAddress = _http.BaseAddress.ToString();
    baseAddress = baseAddress.Substring(0, baseAddress.Length - 1);
    return Path.Join(baseAddress, uriBuilder.Path);
  }

  public async Task<List<ClusterResponse>> GetAgglomerativeClusters(int fileId, bool containsHeaders, List<object> columns, StandarizationMethod standarization, DistanceMetric metric, int noClusters, bool download = false)
  {
    UriBuilder uriBuider = new(new Uri(_http.BaseAddress, $"/{(int)AlgorithmType.CLUSTERING}/files/{fileId}/partitional"));
    string columnString = string.Join("&", columns.Select(c => $"columns={c}").ToList());

    uriBuider.Query = $"contains_headers={containsHeaders.ToString().ToLower()}&{columnString}&standarization={(int)standarization}&download={download.ToString().ToLower()}&metric={(int)metric}&no_clusters={noClusters}";

    return await this._http.GetFromJsonAsync<List<ClusterResponse>>(uriBuider.Uri.ToString());
  }

  public async Task<string> GetPartitionalClustersImg(int fileId, bool containsHeaders, List<object> columns, StandarizationMethod standarization, DistanceMetric metric)
  {
    UriBuilder uriBuilder = new(new Uri(_http.BaseAddress, $"/{(int)AlgorithmType.CLUSTERING}/files/{fileId}/partitional/img"));
    string columnString = string.Join("&", columns.Select(c => $"columns={c}").ToList());

    uriBuilder.Query = $"contains_headers={containsHeaders.ToString().ToLower()}&{columnString}&standarization={(int)standarization}&metric={(int)metric}";

    return await this._http.GetFromJsonAsync<string>(uriBuilder.Uri.ToString());
  }
}