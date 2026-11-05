namespace AdrGuardDemo.Infrastructure.Caching;

public sealed class RedisCatalogCache
{
    public Task<string?> GetAsync(string productId, CancellationToken cancellationToken = default) =>
        Task.FromResult<string?>(null);
}
