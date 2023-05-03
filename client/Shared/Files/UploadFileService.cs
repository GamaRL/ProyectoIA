using System.Net.Http.Headers;
using System.Net.Http.Json;

public class UploadFileService : IUploadFileService
{
  private readonly HttpClient _http;

  public UploadFileService(HttpClient http)
  {
    this._http = http;
  }

  public async Task<FileModel> Upload(Stream file, String fileName, AlgorithmType type)
  {
    MultipartFormDataContent content = new();
    try
    {
      var fileContent = new StreamContent(file);

      fileContent.Headers.ContentType = new MediaTypeHeaderValue("text/csv");

      content.Add(
        content: fileContent,
        name: "file",
        fileName: fileName
      );

    }
    catch (Exception ex)
    {
      Console.WriteLine(ex.ToString());
    }

    var response = await _http.PostAsync($"/{(int)type}/files/", content);

    return await response.Content.ReadFromJsonAsync<FileModel>();
  }

  public long GetMaxFileSize()
  {
    return 20 * 1024L * 1024L;
  }

  public async Task<FileContentModel> GetFileContent(int fileId, AlgorithmType type)
  {
    var response = await this._http.GetAsync($"{(int)type}/files/{fileId}");
    return  await response.Content.ReadFromJsonAsync<FileContentModel>();
  }

  public async Task<List<FileModel>> GetFiles(AlgorithmType type)
  {
    var response = await this._http.GetAsync($"{(int)type}/files");
    return await response.Content.ReadFromJsonAsync<List<FileModel>>();
  }

  public string GetFileUrl(int fileId, AlgorithmType type)
  {
    UriBuilder uriBuider = new(new Uri(_http.BaseAddress, $"/{(int)type}/files/{fileId}"));
    uriBuider.Query = "download=true";
    return uriBuider.Uri.ToString();
  }

  public async Task<FileModel> RemoveFile(int id, AlgorithmType type)
  {
    var response = await this._http.DeleteAsync($"{(int)type}/files/{id}");
    return await response.Content.ReadFromJsonAsync<FileModel>();
  }

  public async Task<List<object>> GetFileHeaders(int fileId, bool containsHeaders, AlgorithmType type)
  {
    UriBuilder uriBuider = new(new Uri(_http.BaseAddress, $"/{(int)type}/files/{fileId}/headers"));
    uriBuider.Query = $"contains_headers={containsHeaders.ToString().ToLower()}";
    return await this._http.GetFromJsonAsync<List<object>>(uriBuider.Uri.ToString());
  }
  public async Task<FileContentModel> GetFileContentWithHeaders(int fileId, bool containsHeaders, List<object> columns, AlgorithmType type)
  {
    UriBuilder uriBuider = new(new Uri(_http.BaseAddress, $"/{(int)type}/files/{fileId}/content"));
    string columnString = string.Join("&", columns.Select(c => $"columns={c}").ToList());
    uriBuider.Query = $"contains_headers={containsHeaders.ToString().ToLower()}&{columnString}";
    
    return await this._http.GetFromJsonAsync<FileContentModel>(uriBuider.Uri.ToString());
  }
}